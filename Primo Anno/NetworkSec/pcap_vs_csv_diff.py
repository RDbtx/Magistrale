import re
import subprocess
import sys
from pathlib import Path

import pandas as pd


# =====================================
# ---         Configuration         ---
# =====================================

BASE_DIR    = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "src/model/dataset"
KEYLOG      = str(BASE_DIR / "src/model/dataset/ssl keys/all.txt")
OUT_DIR     = BASE_DIR / "diff_results"

# 4-http-stream excluded (dropped from training — too few samples)
ATTACK_FOLDERS = [
    "1-http-flood",
    "2-fuzzing",
    "3-http-loris",
    "5-quic-flood",
    "6-quic-loris",
    "7-quic-enc",
    "8-http-smuggle",
    "9-http2-concurrent",
    "10-http2-pause",
]

SERVERS = ["caddy", "cloudflare", "h2o", "litespeed", "nginx", "windows"]

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

COL_W = 44

DIFF_MARKER = {
    "=":       "     =",
    "MISSING": "◄ MISSING",
    "EXTRA":   "► EXTRA  ",
    "DIFF":    "✗ DIFF   ",
}


# =====================================
# ---   Value Normalisation Helpers  -
# =====================================

def is_null(v) -> bool:
    """
    Returns True if the value is considered null: None, float NaN, or blank string.

    Inputs:
    - v: Value to check.

    Output:
    - result: True if the value is null, False otherwise.
    """
    if v is None:
        return True
    if isinstance(v, float) and pd.isna(v):
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    return False


def fmt(v) -> str:
    """
    Formats a value as a display string, returning 'NULL' for null values.

    Inputs:
    - v: Value to format.

    Output:
    - result: 'NULL' if the value is null, otherwise its stripped string representation.
    """
    return "NULL" if is_null(v) else str(v).strip()


def normalise_flag(v) -> str:
    """
    Normalises a flag value to the canonical string '0' or '1'.

    Inputs:
    - v: Flag value in any supported representation.

    Output:
    - result: '1' if the value is truthy, '0' otherwise.
    """
    if isinstance(v, bool):
        return "1" if v else "0"
    s = str(v).strip().lower()
    if s in ("true", "1"):
        return "1"
    if s in ("false", "0"):
        return "0"
    if s.startswith("0x"):
        try:
            return "1" if int(s, 16) != 0 else "0"
        except ValueError:
            pass
    try:
        return "1" if float(s) != 0 else "0"
    except ValueError:
        pass
    return "0"


def sum_multival(s: str) -> float:
    """
    Sums a '+'-joined multi-value string and returns the total as a float.

    Inputs:
    - s: String of '+'-separated numeric values.

    Output:
    - total: Numeric sum, or None if parsing fails.
    """
    try:
        return sum(float(x.strip()) for x in s.split("+") if x.strip())
    except (ValueError, TypeError):
        return None


def values_equal(feat: str, a, b) -> bool:
    """
    Compares two feature values using semantics appropriate for the feature type:
    binary flags use normalised flag comparison, multi-value fields are summed,
    numeric strings are compared as floats, and all others as plain strings.

    Inputs:
    - feat: Feature name used to select the comparison strategy.
    - a: First value to compare.
    - b: Second value to compare.

    Output:
    - equal: True if the values are considered equal, False otherwise.
    """
    a_null, b_null = is_null(a), is_null(b)
    if a_null and b_null:
        return True
    if a_null != b_null:
        return False

    a_s, b_s = str(a).strip(), str(b).strip()

    if feat in BINARY_FLAG_COLS:
        return normalise_flag(a_s) == normalise_flag(b_s)

    if feat in MULTI_VALUE_FEATURES:
        fa, fb = sum_multival(a_s), sum_multival(b_s)
        if fa is not None and fb is not None:
            return abs(fa - fb) < 1e-6
        return a_s == b_s

    try:
        return abs(float(a_s) - float(b_s)) < 1e-6
    except (ValueError, TypeError):
        pass

    return a_s == b_s


# =====================================
# ---        CSV Loading            ---
# =====================================

def load_csv_rows(csv_path: str, n: int) -> list:
    """
    Loads up to n data rows from a dataset CSV as raw strings, preventing
    pandas from silently converting values through type inference.

    Inputs:
    - csv_path: Path to the CSV file to load.
    - n: Maximum number of rows to read.

    Output:
    - rows: List of dictionaries mapping each feature name to its raw string value or None.
    """
    df = pd.read_csv(
        csv_path,
        nrows=n,
        dtype=str,
        on_bad_lines="skip",
        low_memory=False,
        keep_default_na=False,
        na_values=[""],
    )
    df.columns = [c.strip() for c in df.columns]
    rows = []
    for _, series in df.iterrows():
        row = {}
        for feat in FEATURES:
            raw = series.get(feat)
            if isinstance(raw, float) and pd.isna(raw):
                raw = None
            elif isinstance(raw, str):
                raw = raw.strip() or None
            row[feat] = raw
        rows.append(row)
    return rows


# =====================================
# ---     tshark Extraction         ---
# =====================================

def find_tshark() -> str:
    """
    Locates the tshark executable by checking PATH and known installation paths.

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
    for p in ("/usr/bin/tshark", "/usr/local/bin/tshark",
              r"C:\Program Files\Wireshark\tshark.exe"):
        if Path(p).exists():
            return p
    raise FileNotFoundError("tshark not found. Install Wireshark/tshark.")


def postprocess(raw: str) -> str:
    """
    Applies the three-step post-processing pipeline to raw tshark output.
    Order is mandatory: comma→plus, then strip quotes, then pipe→comma.

    Inputs:
    - raw: Raw string output from tshark.

    Output:
    - result: Cleaned string ready for CSV parsing.
    """
    result = raw.replace(",", "+")
    result = result.replace('"', "")
    result = result.replace(SEP, ",")
    return result


def extract_tshark_packets(pcap: str, keylog: str, n: int) -> list:
    """
    Runs tshark on a pcap file and extracts all FEATURES for up to n packets.

    Inputs:
    - pcap: Path to the input pcap file.
    - keylog: Path to the TLS keylog file, or None.
    - n: Maximum number of packets to extract.

    Output:
    - results: List of (feature_dict, ['tshark']) tuples, one per extracted packet.
    """
    tshark = find_tshark()
    print(f"[diff] tshark: {tshark}")

    cmd = [tshark, "-r", pcap, "-T", "fields",
           "-E", f"separator={SEP}",
           "-E", "header=y",
           "-E", "quote=d"]
    if keylog and Path(keylog).exists():
        cmd += ["-o", f"tls.keylog_file:{keylog}"]
    else:
        print("[diff] WARN: keylog not found — TLS fields will be empty")
    for feat in FEATURES:
        cmd += ["-e", feat]

    print(f"[diff] Running tshark on {Path(pcap).name} ...")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        for line in proc.stderr.strip().splitlines()[:10]:
            print(f"       {line}")
        raise RuntimeError(f"tshark exited with code {proc.returncode}")

    stderr_lines = proc.stderr.strip().splitlines() if proc.stderr.strip() else []
    if stderr_lines:
        print(f"[diff] tshark warnings ({len(stderr_lines)} lines, first 5):")
        for line in stderr_lines[:5]:
            print(f"       {line}")

    clean = postprocess(proc.stdout)
    lines = clean.strip().splitlines()
    if len(lines) < 2:
        for line in proc.stdout.splitlines()[:3]:
            print(f"       {repr(line)}")
        raise RuntimeError("tshark produced no data rows after post-processing.")

    header = [c.strip() for c in lines[0].split(",")]
    print(f"[diff] tshark header: {len(header)} columns (expected {len(FEATURES)})")

    results = []
    for line in lines[1: n + 1]:
        parts = line.split(",")
        while len(parts) < len(header):
            parts.append("")
        row_raw = dict(zip(header, parts))
        row = {
            feat: (row_raw.get(feat, "").strip() or None)
            for feat in FEATURES
        }
        results.append((row, ["tshark"]))

    print(f"[diff] extracted {len(results)} rows")
    return results


# =====================================
# ---     Alignment and Comparison  ---
# =====================================

def is_aligned(csv_row: dict, pkt_row: dict) -> bool:
    """
    Checks whether a CSV row and a packet row are aligned by comparing frame.len.

    Inputs:
    - csv_row: Feature dictionary loaded from the dataset CSV.
    - pkt_row: Feature dictionary extracted from the pcap file.

    Output:
    - aligned: True if frame.len values match, False otherwise.
    """
    return values_equal("frame.len", csv_row.get("frame.len"), pkt_row.get("frame.len"))


def compare_rows(csv_row: dict, pkt_row: dict) -> list:
    """
    Compares all FEATURES between a CSV row and an extracted packet row.

    Inputs:
    - csv_row: Feature dictionary loaded from the dataset CSV.
    - pkt_row: Feature dictionary extracted from the pcap file.

    Output:
    - results: List of (feature, csv_value, extracted_value, diff_type) tuples.
               diff_type is one of '=', 'MISSING', 'EXTRA', or 'DIFF'.
    """
    results = []
    for feat in FEATURES:
        csv_v = csv_row.get(feat)
        pkt_v = pkt_row.get(feat)
        equal = values_equal(feat, csv_v, pkt_v)

        if equal:
            diff_type = "="
        elif is_null(csv_v) and not is_null(pkt_v):
            diff_type = "EXTRA"
        elif not is_null(csv_v) and is_null(pkt_v):
            diff_type = "MISSING"
        else:
            diff_type = "DIFF"

        results.append((feat, fmt(csv_v), fmt(pkt_v), diff_type))
    return results


# =====================================
# ---      Report Formatting        ---
# =====================================

def format_header(pkt_idx: int, csv_idx: int, layers: list, aligned: bool) -> str:
    """
    Formats the header block for a single packet comparison section.

    Inputs:
    - pkt_idx: Packet index in the pcap file.
    - csv_idx: Corresponding row index in the CSV file.
    - layers: List of source label strings for the packet.
    - aligned: Whether the frame.len values matched between the two sources.

    Output:
    - header: Formatted header string.
    """
    align_warn = "  ⚠ ALIGNMENT MISMATCH — frame.len differs" if not aligned else ""
    sep = "─" * (COL_W * 2 + 52)
    return (
        f"\n{sep}\n"
        f"  Packet #{pkt_idx}  (CSV row #{csv_idx})   layers: {layers}{align_warn}\n"
        f"{sep}\n"
        f"  {'FEATURE':<42}  {'CSV (tshark)':<{COL_W}}  {'EXTRACTED':<{COL_W}}  STATUS\n"
        f"{'─' * (COL_W * 2 + 52)}\n"
    )


def format_row_line(feat: str, csv_v: str, pkt_v: str, diff_type: str) -> str:
    """
    Formats a single feature comparison line for the report.

    Inputs:
    - feat: Feature name.
    - csv_v: Formatted CSV value string.
    - pkt_v: Formatted extracted value string.
    - diff_type: One of '=', 'MISSING', 'EXTRA', or 'DIFF'.

    Output:
    - line: Formatted comparison line string.
    """
    marker = DIFF_MARKER.get(diff_type, diff_type)
    return f"  {feat:<42}  {csv_v:<{COL_W}}  {pkt_v:<{COL_W}}  {marker}\n"


def build_report(comparisons: list, skip_equal: bool) -> str:
    """
    Assembles the full diff report from all packet comparisons, including a summary.

    Inputs:
    - comparisons: List of (pkt_idx, csv_idx, layers, aligned, cmp) tuples.
    - skip_equal: If True, exact-match rows are omitted from the output.

    Output:
    - report: Full diff report as a formatted string.
    """
    lines = []

    total_feats = 0
    counts = {"=": 0, "MISSING": 0, "EXTRA": 0, "DIFF": 0}
    per_feat = {f: {"MISSING": 0, "EXTRA": 0, "DIFF": 0} for f in FEATURES}
    align_mismatches = 0

    for pkt_idx, csv_idx, layers, aligned, cmp in comparisons:
        if not aligned:
            align_mismatches += 1
        lines.append(format_header(pkt_idx, csv_idx, layers, aligned))

        for feat, csv_v, pkt_v, diff_type in cmp:
            total_feats += 1
            counts[diff_type] = counts.get(diff_type, 0) + 1
            if diff_type != "=":
                per_feat[feat][diff_type] = per_feat[feat].get(diff_type, 0) + 1
            if skip_equal and diff_type == "=":
                continue
            lines.append(format_row_line(feat, csv_v, pkt_v, diff_type))

    sep = "═" * (COL_W * 2 + 52)
    lines.append(f"\n{sep}\n  SUMMARY\n{sep}\n")
    lines.append(f"  Packets compared          : {len(comparisons)}\n")
    lines.append(f"  Alignment mismatches      : {align_mismatches}"
                 + ("  ← rows may be offset; check frame.len\n" if align_mismatches else "\n"))
    lines.append(f"\n  Total feature comparisons : {total_feats}\n")
    for dtype, label in [("=", "Exact matches"), ("DIFF", "Value differs (both present)"),
                         ("MISSING", "Missing in extractor"), ("EXTRA", "Extra in extractor")]:
        cnt = counts.get(dtype, 0)
        pct = 100 * cnt / total_feats if total_feats else 0
        lines.append(f"  {label:<34}: {cnt:>6}  ({pct:.1f}%)\n")

    problem_feats = [(f, d) for f, d in per_feat.items() if any(d.values())]
    if problem_feats:
        lines.append(f"\n  Per-feature breakdown ({len(problem_feats)} features with issues):\n")
        lines.append(f"  {'FEATURE':<50}  {'MISSING':>8}  {'EXTRA':>7}  {'DIFF':>6}\n")
        lines.append(f"  {'─'*50}  {'─'*8}  {'─'*7}  {'─'*6}\n")
        problem_feats.sort(key=lambda x: -sum(x[1].values()))
        for feat, d in problem_feats:
            lines.append(f"  {feat:<50}  {d['MISSING']:>8}  {d['EXTRA']:>7}  {d['DIFF']:>6}\n")

    lines.append(
        f"\n  NOTE: Alignment is verified via frame.len on every row.\n"
        f"  MISSING = CSV has value, extractor returned NULL.\n"
        f"  EXTRA   = Extractor found value, CSV was NULL.\n"
        f"  DIFF    = Both have values but they differ numerically or as strings.\n"
    )
    return "".join(lines)


# =====================================
# ---       Single-File Runner      ---
# =====================================

def run(pcap: str, csv: str, keylog: str, n: int,
        out: str, skip_equal: bool, no_align_check: bool) -> None:
    """
    Runs the diff comparison between a single PCAP file and its corresponding CSV.

    Inputs:
    - pcap: Path to the input pcap file.
    - csv: Path to the corresponding dataset CSV file.
    - keylog: Path to the TLS keylog file, or None.
    - n: Number of packets to compare.
    - out: Output file path for the report, or empty string to print to stdout.
    - skip_equal: If True, exact-match rows are omitted from the report.
    - no_align_check: If True, skips frame.len alignment verification.
    """
    print(f"[diff] PCAP    : {pcap}")
    print(f"[diff] CSV     : {csv}")
    print(f"[diff] Keylog  : {keylog or '(none)'}")
    print(f"[diff] Packets : {n}")

    csv_rows = load_csv_rows(csv, n)
    print(f"[diff] CSV rows loaded: {len(csv_rows)}")

    extracted = extract_tshark_packets(pcap, keylog, n)

    limit = min(len(csv_rows), len(extracted))
    if limit < n:
        print(f"[diff] WARN: only {limit} rows available "
              f"(CSV: {len(csv_rows)}, extracted: {len(extracted)})")

    comparisons = []
    for i in range(limit):
        csv_row = csv_rows[i]
        pkt_row, layers = extracted[i]
        aligned = no_align_check or is_aligned(csv_row, pkt_row)
        if not aligned:
            print(f"  [diff] WARN packet {i+1}: frame.len mismatch "
                  f"(csv={fmt(csv_row.get('frame.len'))} "
                  f"extracted={fmt(pkt_row.get('frame.len'))})")
        cmp = compare_rows(csv_row, pkt_row)
        comparisons.append((i + 1, i + 1, layers, aligned, cmp))

    report = build_report(comparisons, skip_equal)
    if out:
        Path(out).write_text(report, encoding="utf-8")
        print(f"[diff] Report saved to: {out}")
    else:
        print(report)


# =====================================
# ---         Batch Runner          ---
# =====================================

def count_csv_rows(csv_path: Path) -> int:
    """
    Returns the number of data rows in a CSV file by reading only the frame.len column.

    Inputs:
    - csv_path: Path to the CSV file.

    Output:
    - count: Number of data rows, or 0 if the file cannot be read.
    """
    try:
        df = pd.read_csv(csv_path, usecols=["frame.len"],
                         on_bad_lines="skip", low_memory=False)
        return len(df)
    except Exception:
        return 0


def run_batch() -> None:
    """
    Iterates over all PCAP/CSV pairs in ATTACK_FOLDERS × SERVERS, runs the full
    diff on each pair, and writes per-file reports and a consolidated summary to OUT_DIR.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pairs = []
    for folder in ATTACK_FOLDERS:
        attack_num = folder.split("-")[0]
        for server in SERVERS:
            csv = DATASET_DIR / folder / f"pcap{attack_num}-{server}.csv"

            pcap_standard = DATASET_DIR / folder / f"pcap{attack_num}-{server}.pcap"
            pcap_new      = DATASET_DIR / folder / f"pcap{attack_num}-{server}-new.pcap"
            if pcap_standard.exists():
                pcap = pcap_standard
            elif pcap_new.exists():
                pcap = pcap_new
                print(f"[batch] NOTE: using {pcap.name} (non-standard name)")
            else:
                print(f"[batch] SKIP (no pcap): pcap{attack_num}-{server}.pcap")
                continue

            if not csv.exists():
                print(f"[batch] SKIP (no csv):  {csv.name}")
                continue
            pairs.append((folder, server, pcap, csv))

    print(f"\n[batch] Found {len(pairs)} PCAP/CSV pairs to process")
    print(f"[batch] Output directory: {OUT_DIR}\n")

    summary_lines = [
        "=" * 90,
        "  FULL DATASET DIFF SUMMARY — tshark mode, all PCAP/CSV pairs",
        "  4-http-stream excluded (dropped from training)",
        "=" * 90,
        f"\n  {'FILE':<40}  {'PACKETS':>8}  {'EXACT%':>7}  "
        f"{'ALIGN':>6}  {'DIFF':>6}  {'MISSING':>8}  {'EXTRA':>6}",
        "  " + "─" * 86,
    ]

    total_comparisons = total_exact = total_diff = 0
    total_missing = total_extra = total_align = 0

    for idx, (folder, server, pcap, csv) in enumerate(pairs, 1):
        attack_num = folder.split("-")[0]
        label = f"pcap{attack_num}-{server}"
        print(f"[batch] {idx}/{len(pairs)}  {folder}/{label} ...", flush=True)

        n_rows = count_csv_rows(csv)
        if n_rows == 0:
            print(f"[batch]   WARN: could not count rows in {csv.name}, skipping")
            continue

        file_out_dir = OUT_DIR / folder
        file_out_dir.mkdir(parents=True, exist_ok=True)
        out_path = file_out_dir / f"{label}.txt"

        try:
            run(
                pcap=str(pcap),
                csv=str(csv),
                keylog=KEYLOG if Path(KEYLOG).exists() else None,
                n=n_rows,
                out=str(out_path),
                skip_equal=True,
                no_align_check=False,
            )
        except Exception as exc:
            print(f"[batch]   ERROR: {exc}")
            summary_lines.append(f"  {label:<40}  ERROR: {exc}")
            continue

        try:
            text = out_path.read_text(encoding="utf-8")

            def extract_int(pattern: str) -> int:
                m = re.search(pattern, text)
                return int(m.group(1).replace(",", "")) if m else 0

            pkts      = extract_int(r"Packets compared\s+:\s+([\d,]+)")
            align     = extract_int(r"Alignment mismatches\s+:\s+([\d,]+)")
            feats     = extract_int(r"Total feature comparisons\s+:\s+([\d,]+)")
            exact     = extract_int(r"Exact matches\s+:\s+([\d,]+)")
            diff_cnt  = extract_int(r"Value differs \(both present\)\s+:\s+([\d,]+)")
            miss_cnt  = extract_int(r"Missing in extractor\s+:\s+([\d,]+)")
            extra_cnt = extract_int(r"Extra in extractor\s+:\s+([\d,]+)")

            exact_pct = 100 * exact / feats if feats else 0
            total_comparisons += feats
            total_exact       += exact
            total_diff        += diff_cnt
            total_missing     += miss_cnt
            total_extra       += extra_cnt
            total_align       += align

            align_str = str(align) if align == 0 else f"⚠ {align}"
            summary_lines.append(
                f"  {label:<40}  {pkts:>8,}  {exact_pct:>6.1f}%"
                f"  {align_str:>6}  {diff_cnt:>6,}  {miss_cnt:>8,}  {extra_cnt:>6,}"
            )
            print(f"[batch]   packets={pkts:,}  exact={exact_pct:.1f}%  "
                  f"align_err={align}  diff={diff_cnt}  miss={miss_cnt}  extra={extra_cnt}")

        except Exception as exc:
            print(f"[batch]   WARN: could not parse report for {label}: {exc}")
            summary_lines.append(f"  {label:<40}  (could not parse report)")

    overall_pct = 100 * total_exact / total_comparisons if total_comparisons else 0
    summary_lines += [
        "  " + "─" * 86,
        f"  {'TOTAL':<40}  {'':>8}  {overall_pct:>6.1f}%"
        f"  {total_align:>6}  {total_diff:>6,}  {total_missing:>8,}  {total_extra:>6,}",
        f"\n  Total feature comparisons : {total_comparisons:,}",
        f"  Exact matches             : {total_exact:,}  ({overall_pct:.2f}%)",
        f"  Alignment mismatches      : {total_align}",
        f"  DIFF                      : {total_diff:,}",
        f"  MISSING                   : {total_missing:,}",
        f"  EXTRA                     : {total_extra:,}",
    ]

    summary_text = "\n".join(summary_lines) + "\n"
    summary_path = OUT_DIR / "summary.txt"
    summary_path.write_text(summary_text, encoding="utf-8")

    print(f"\n[batch] Done.")
    print(f"[batch] Summary written to: {summary_path}")
    print(f"[batch] Overall exact match: {overall_pct:.2f}% across {total_comparisons:,} comparisons")
    print(summary_text)


# =====================================
# ---       Main Execution          ---
# =====================================

if __name__ == "__main__":
    run_batch()