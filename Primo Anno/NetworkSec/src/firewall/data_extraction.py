import os
import platform
import queue
import subprocess
import sys
import threading
from pathlib import Path
import pandas as pd


# =====================================
# ---         Configuration         ---
# =====================================

FEATURES = [
    "frame.len", "ip.len", "tcp.len", "tcp.hdr_len", "tcp.flags.ack",
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
    "http.content_length", "http.content_type",
]

SEP = "|"
DEFAULT_KEYLOG = "/tmp/sslkeys.log"


# =====================================
# ---   tshark Helper Functions     ---
# =====================================

def find_tshark() -> str:
    """
    Locates the tshark executable by checking the TSHARK environment variable,
    then PATH, then a set of known installation locations.

    Output:
    - tshark_path: Absolute path to the tshark executable.
    """
    env = os.environ.get("TSHARK")
    if env:
        return env
    cmd = "where" if sys.platform == "win32" else "which"
    try:
        r = subprocess.run([cmd, "tshark"], capture_output=True, text=True)
        found = r.stdout.strip().splitlines()
        if found:
            return found[0]
    except FileNotFoundError:
        pass
    for p in ("/usr/bin/tshark", "/usr/local/bin/tshark",
              r"C:\Program Files\Wireshark\tshark.exe"):
        if Path(p).exists():
            return p
    raise FileNotFoundError(
        "tshark not found. Install Wireshark/tshark or set the TSHARK env variable."
    )


def get_supported_fields(tshark: str) -> set:
    """
    Queries tshark for its full field registry and returns the set of supported
    field names, used to skip FEATURES entries the installed version does not recognise.

    Inputs:
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


def postprocess_line(raw: str) -> str:
    """
    Applies the three-step post-processing pipeline to a raw tshark output line.
    Order is mandatory: comma→plus first, then strip quotes, then pipe→comma last.

    Inputs:
    - raw: Raw string line from tshark output.

    Output:
    - result: Cleaned string ready for CSV parsing.
    """
    result = raw.replace(",", "+")
    result = result.replace('"', "")
    result = result.replace(SEP, ",")
    return result


def parse_row(header_cols: list, processed_line: str, valid_features: list) -> dict:
    """
    Splits one post-processed CSV line and returns a dict keyed by FEATURES.
    Missing or empty values become None. Features unsupported by the installed
    tshark version are always None.

    Inputs:
    - header_cols: Ordered list of column names from the tshark header line.
    - processed_line: A single post-processed tshark data line.
    - valid_features: List of features confirmed supported by the installed tshark.

    Output:
    - row: Dictionary mapping each feature name to its extracted value or None.
    """
    parts = processed_line.split(",")
    while len(parts) < len(header_cols):
        parts.append("")
    row_raw = dict(zip(header_cols, parts))

    row = {}
    for feat in FEATURES:
        if feat in valid_features:
            val = row_raw.get(feat, "").strip()
            row[feat] = val if val else None
        else:
            row[feat] = None
    return row


def extract_source_ip(header_cols: list, raw_line: str) -> str:
    """
    Extracts the ip.src or ipv6.src value from a raw tshark line before
    post-processing. Must be called on the raw line because comma→plus
    substitution would corrupt IP address strings.
    ip.src and ipv6.src are appended after FEATURES in the tshark command.

    Inputs:
    - header_cols: Ordered list of column names from the tshark header line.
    - raw_line: Unprocessed tshark output line.

    Output:
    - source_ip: Extracted source IP string, or None if not present.
    """
    parts_raw = raw_line.replace('"', "").split(SEP)
    row_raw = dict(zip(header_cols, parts_raw))
    ip = row_raw.get("ip.src") or row_raw.get("ipv6.src")
    if ip:
        ip = ip.strip()
    return ip if ip else None


# =====================================
# ---         Live Capture          ---
# =====================================

class LiveCapture:
    """
    Captures live packets from a network interface using tshark and places each
    packet as a (source_ip, raw_df) tuple on a queue for firewall_engine.py to consume.
    Raw DataFrames are unpreprocessed and fed into LivePreprocessor.preprocess()
    in firewall_engine.py before model inference.

    Inputs:
    - interface: Network interface name to capture from.
    - bpf_filter: Optional BPF capture filter string.
    - keylog_file: Path to an NSS SSLKEYLOGFILE for live TLS decryption.
    - tshark_bin: Explicit tshark binary path; auto-detected if None.
    """

    def __init__(
            self,
            interface: str,
            bpf_filter: str = None,
            keylog_file: str = None,
            tshark_bin: str = None,
    ) -> None:
        if interface is None:
            interface = "eth0" if platform.system() in ("Windows", "Linux") else "en0"

        self.interface = interface
        self.bpf_filter = bpf_filter
        self.queue: queue.Queue = queue.Queue()
        self.stop_event = threading.Event()
        self.thread: threading.Thread = None

        self.tshark = tshark_bin or find_tshark()
        supported = get_supported_fields(self.tshark)
        self.valid_features = [f for f in FEATURES if f in supported]
        invalid = [f for f in FEATURES if f not in supported]
        if invalid:
            print(f"[LiveCapture] WARN: {len(invalid)} unsupported fields "
                  f"will be NULL: {invalid}")

        self.keylog_file = keylog_file or DEFAULT_KEYLOG
        if not os.path.exists(self.keylog_file):
            open(self.keylog_file, "a").close()
        os.environ["SSLKEYLOGFILE"] = self.keylog_file


    # =====================================
    # ---      Capture Loop Internals   ---
    # =====================================

    def build_cmd(self) -> list:
        """
        Builds the tshark command list for live capture with the configured
        interface, features, filter, and keylog settings.

        Output:
        - cmd: List of command-line arguments for subprocess.Popen.
        """
        cmd = [
            self.tshark,
            "-i", self.interface,
            "-l",
            "-T", "fields",
            "-E", f"separator={SEP}",
            "-E", "header=y",
            "-E", "quote=d",
            "-E", "occurrence=a",
        ]
        if self.bpf_filter:
            cmd += ["-f", self.bpf_filter]
        cmd += ["-o", f"tls.keylog_file:{self.keylog_file}"]
        for feat in self.valid_features:
            cmd += ["-e", feat]
        cmd += ["-e", "ip.src", "-e", "ipv6.src"]
        return cmd

    def capture_loop(self) -> None:
        """
        Runs tshark as a subprocess, reads its output line by line,
        parses each packet into a raw DataFrame, and places it on the queue.
        Runs until stop_event is set.
        """
        cmd = self.build_cmd()
        print(f"[LiveCapture] interface  = {self.interface}")
        print(f"[LiveCapture] keylog     = {self.keylog_file}")
        print(f"[LiveCapture] tshark     = {self.tshark}")
        if self.bpf_filter:
            print(f"[LiveCapture] bpf_filter = {self.bpf_filter}")
        print(f"[LiveCapture] features   = "
              f"{len(self.valid_features)} / {len(FEATURES)} supported")

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        header_cols = []
        seen = 0
        errors = 0

        try:
            for raw_line in proc.stdout:
                if self.stop_event.is_set():
                    break

                raw_line = raw_line.rstrip("\n")
                if not raw_line:
                    continue

                if not header_cols:
                    clean_header = raw_line.replace('"', "").replace(SEP, ",")
                    header_cols = [c.strip() for c in clean_header.split(",")]
                    print(f"[LiveCapture] tshark started: "
                          f"{len(header_cols)} columns")
                    continue

                source_ip = extract_source_ip(header_cols, raw_line)

                try:
                    processed = postprocess_line(raw_line)
                    row = parse_row(header_cols, processed, self.valid_features)
                    raw_df = pd.DataFrame([row], columns=FEATURES)
                    self.queue.put((source_ip, raw_df))
                    seen += 1
                except Exception as exc:
                    errors += 1
                    if errors <= 10:
                        print(f"[LiveCapture] error (pkt {seen + errors}): {exc}")

        except Exception as exc:
            print(f"[LiveCapture] fatal loop error: {exc}")

        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
            stderr_out = proc.stderr.read() if proc.stderr else ""
            if stderr_out.strip():
                lines = stderr_out.strip().splitlines()
                print(f"[LiveCapture] tshark warnings "
                      f"({len(lines)} lines, first 5):")
                for line in lines[:5]:
                    print(f"    {line}")
            print(f"[LiveCapture] stopped — packets={seen}, errors={errors}")


    # =====================================
    # ---          Public API           ---
    # =====================================

    def start(self) -> None:
        """
        Starts live packet capture in a background daemon thread.
        """
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.thread.start()
        print(f"[LiveCapture] capture thread started on [{self.interface}]")

    def stop(self) -> None:
        """
        Signals the capture loop to stop and waits for the thread to finish.
        """
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=10)
        print("[LiveCapture] stopped.")