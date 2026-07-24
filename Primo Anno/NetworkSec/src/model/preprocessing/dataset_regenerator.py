import csv
import os
import pathlib
import subprocess
import sys
from pathlib import Path

# =====================================
# ---         Configuration         ---
# =====================================

MODEL_DIR = pathlib.Path(__file__).parent.parent
OUTPUT_FOLDER = os.path.join(MODEL_DIR, "new_dataset")
DATASET_FOLDER = os.path.join(MODEL_DIR, "dataset")
SSLKEYS = os.path.join(MODEL_DIR, "dataset/ssl keys/all.txt")

PREFILTERING_FEATURES = [
    "frame.len", "frame.time_relative", "ip.len", "ip.src", "ip.dst", "tcp.len", "tcp.hdr_len", "tcp.flags.ack",
    "tcp.flags.push", "tcp.flags.reset", "tcp.flags.syn", "tcp.flags.fin",
    "tcp.window_size_value", "tcp.option_len", "udp.length", "tls.record.length",
    "tls.reassembled.length", "tls.handshake.length", "tls.handshake.certificates_length",
    "tls.handshake.certificate_length", "tls.handshake.session_id_length",
    "tls.handshake.cipher_suites_length", "tls.handshake.extensions_length",
    "tls.handshake.client_cert_vrfy.sig_len", "quic.packet_length", "quic.long.packet_type",
    "quic.packet_number_length", "quic.length", "quic.nci.connection_id.length",
    "quic.crypto.length", "quic.fixed_bit", "quic.spin_bit", "quic.stream.fin",
    "quic.stream.len", "quic.token_length", "quic.padding_length", "http2.length",
    "http2.header.length", "http2.header.name.length", "http2.header.value.length",
    "http2.headers.content_length", "http3.frame_length",
    "http3.settings.qpack.max_table_capacity", "http3.settings.max_field_section_size",
    "dns.flags.response", "dns.count.queries", "dns.count.answers",
    "http.content_length", "http.content_type", "http.host", "udp.dstport", "dns.id", "urlencoded-form.key"
]

MULTI_VALUE_FEATURES = {
    "tcp.option_len",
    "tls.record.length",
    "tls.handshake.length",
    "tls.handshake.certificate_length",
    "tls.handshake.extensions_length",
    "http2.length",
    "http2.header.name.length",
    "http2.header.value.length",
}

BINARY_FLAG_COLS = {
    "tcp.flags.ack", "tcp.flags.push", "tcp.flags.reset",
    "tcp.flags.syn", "tcp.flags.fin",
    "quic.fixed_bit", "quic.spin_bit", "quic.stream.fin",
    "dns.flags.response",
}

SEP = "|"


# =====================================
# ---   tshark Discovery Functions  ---
# =====================================

def find_tshark() -> str:
    """
    Locates the tshark executable on the current system by checking the PATH
    and a set of known installation paths.

    Output:
    - tshark_path: Absolute path to the tshark executable.
    """
    cmd = "where" if sys.platform == "win32" else "which"
    try:
        r = subprocess.run([cmd, "tshark"], capture_output=True, text=True)
        found = r.stdout.strip().splitlines()
        if found:
            return found[0]
    except FileNotFoundError:
        pass

    for p in (
            "/usr/bin/tshark",
            "/usr/local/bin/tshark",
            r"C:\Program Files\Wireshark\tshark.exe",
    ):
        if Path(p).exists():
            return p

    raise FileNotFoundError("tshark not found. Install Wireshark/tshark.")


def get_supported_fields(tshark: str) -> set:
    """
    Queries tshark for all supported dissector field names.

    Input:
    - tshark: Path to the tshark executable.

    Output:
    - supported: Set of field name strings supported by the installed tshark version.
    """
    proc = subprocess.run(
        [tshark, "-G", "fields"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=True,
    )

    supported = set()
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[0] == "F":
            supported.add(parts[2].strip())
    return supported


# =====================================
# ---   Packet Extraction Functions  ---
# =====================================

def postprocess(raw: str) -> str:
    """
    Cleans raw tshark output by replacing commas with plus signs, stripping
    quotes, and converting the pipe separator back to commas.

    Input:
    - raw: Raw string output from tshark.

    Output:
    - result: Cleaned string ready for CSV parsing.
    """
    result = raw.replace(",", "+")
    result = result.replace('"', "")
    result = result.replace(SEP, ",")
    return result


def extract_tshark_packets(pcap: str, keylog: str = None, n: int = None) -> list:
    """
    Runs tshark on a pcap file and extracts packet fields defined in
    PREFILTERING_FEATURES into a list of row dictionaries.

    Inputs:
    - pcap: Path to the input pcap file.
    - keylog: Optional path to a TLS keylog file for decryption.
    - n: Optional maximum number of packets to extract.

    Output:
    - results: List of tuples where each tuple contains a row dictionary
               mapping feature names to values, and a list with the source label.

    """
    tshark = find_tshark()
    supported = get_supported_fields(tshark)

    valid_features = [f for f in PREFILTERING_FEATURES if f in supported]
    invalid_features = [f for f in PREFILTERING_FEATURES if f not in supported]

    if invalid_features:
        print("[!] Unsupported features skipped:")
        for f in invalid_features:
            print(f"    - {f}")

    cmd = [
        tshark, "-r", pcap, "-T", "fields",
        "-E", f"separator={SEP}",
        "-E", "header=y",
        "-E", "quote=d",
        "-E", "occurrence=a",
    ]

    if keylog and Path(keylog).exists():
        cmd += ["-o", f"tls.keylog_file:{keylog}"]
    else:
        print("[!] WARN: keylog not found — TLS fields may be empty")

    for feat in valid_features:
        cmd += ["-e", feat]

    print(f">>> Running tshark on {Path(pcap).name} ...")
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )

    if proc.returncode != 0:
        for line in proc.stderr.strip().splitlines()[:10]:
            print(f"    {line}")
        raise RuntimeError(f"tshark exited with code {proc.returncode}")

    stderr_lines = proc.stderr.strip().splitlines() if proc.stderr.strip() else []
    if stderr_lines:
        print(f"[!] tshark warnings ({len(stderr_lines)} lines, first 5):")
        for line in stderr_lines[:5]:
            print(f"    {line}")

    clean = postprocess(proc.stdout)
    lines = clean.strip().splitlines()

    if len(lines) < 2:
        for line in proc.stdout.splitlines()[:3]:
            print(f"    RAW: {repr(line)}")
        raise RuntimeError("tshark produced no data rows after post-processing.")

    header = [c.strip() for c in lines[0].split(",")]

    limit = n if n is not None else len(lines) - 1
    results = []

    for line in lines[1: limit + 1]:
        parts = line.split(",")
        while len(parts) < len(header):
            parts.append("")

        row_raw = dict(zip(header, parts))

        row = {}
        for feat in PREFILTERING_FEATURES:
            val = row_raw.get(feat, "").strip()
            row[feat] = val if val else None

        results.append((row, ["tshark"]))

    return results


def extract_to_csv(pcap_path: str, output_csv: str, keylog: str) -> None:
    """
    Extracts packet fields from a pcap file using tshark and writes the results
    to a CSV file with columns matching PREFILTERING_FEATURES.

    Inputs:
    - pcap_path: Path to the input pcap file.
    - output_csv: Destination path for the output CSV file.
    - keylog: Path to the TLS keylog file used for decryption.

    """
    rows = extract_tshark_packets(pcap_path, keylog=keylog)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(PREFILTERING_FEATURES)

        for row, _ in rows:
            writer.writerow([row.get(feat, None) for feat in PREFILTERING_FEATURES])

    print(f"    CSV written to: {output_csv}")


# =====================================
# ---  Main Dataset Regeneration    ---
# =====================================

def dataset_regenerator() -> None:
    """
    Iterates over all pcap files in the dataset directory and converts each one
    to a CSV file in the output folder, preserving the original folder structure.
    """
    for folder in os.listdir(DATASET_FOLDER):
        folder_path = os.path.join(DATASET_FOLDER, folder)
        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".pcap"):
                pcap_path = os.path.join(folder_path, file)
                out_name = os.path.join(folder, f"{Path(file).stem}.csv")
                extract_to_csv(
                    pcap_path,
                    os.path.join(OUTPUT_FOLDER, out_name),
                    keylog=SSLKEYS,
                )
