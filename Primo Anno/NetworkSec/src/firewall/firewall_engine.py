import os
import time
import queue
import joblib
import socket
import pandas as pd
import pathlib
import psutil
import subprocess
import platform
from collections import defaultdict, deque

from src.model.preprocessing.scaling import FLAG_COLS, TO_SCALE_COLUMNS
from src.firewall.data_extraction import LiveCapture


# =====================================
# ---         Configuration         ---
# =====================================

SRC_PATH   = pathlib.Path(__file__).parent.parent
MODEL_PATH = os.path.join(SRC_PATH, "firewall/model/Blackwall.joblib")
SCALER_PATH = os.path.join(SRC_PATH, "model/output/scaler.joblib")

TO_BLOCK_IMMEDIATELY = {}
TO_BLOCK_AFTER_N_INSTANCES = {
    "http-flood", "quic-flood", "http-loris", "quic-loris",
    "quic-enc", "http-smuggle", "http2-concurrent", "http2-pause", "fuzzing"
}
DDOS_STRIKES_TO_BLOCK = 100
DDOS_WINDOW_SECONDS   = 60


# =====================================
# ---       Live Preprocessor       ---
# =====================================

class LivePreprocessor:
    """
    Applies the full scaling.py preprocessing pipeline to a single live packet
    DataFrame, using the saved training scaler to ensure feature alignment.

    Input:
    - saved_scaler: Dictionary loaded from scaler.joblib, containing the fitted
                    scaler instance, the ordered list of numeric columns, and the
                    full post-OHE column list.
    """

    def __init__(self, saved_scaler: dict):
        if saved_scaler is not None:
            self.scaler = saved_scaler["scaler"] if isinstance(saved_scaler, dict) else saved_scaler
            self.scaler_columns = (saved_scaler["scaler_columns"]
                                   if isinstance(saved_scaler, dict) else TO_SCALE_COLUMNS)
            self.ohe_columns = (saved_scaler["ohe_columns"]
                                if isinstance(saved_scaler, dict) and "ohe_columns" in saved_scaler
                                else [])
            if not self.ohe_columns:
                raise RuntimeError(
                    "[Preprocessor] scaler.joblib does not contain 'ohe_columns'. "
                    "Re-run scaling.py to regenerate the scaler with OHE column info included."
                )
            print(f"[Preprocessor] Loaded training scaler "
                  f"({len(self.scaler_columns)} scale cols, "
                  f"{len(self.ohe_columns)} OHE cols).")
        else:
            raise RuntimeError(
                "[Preprocessor] No saved scaler found. "
                "Run scaling.py to generate scaler.joblib before starting the firewall."
            )


    # =====================================
    # ---   Preprocessing Step Functions  -
    # =====================================

    def fill_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fills NaN values: FLAG_COLS receive -1, all remaining NaN cells receive 0.

        Input:
        - df: Raw packet DataFrame with potential NaN values.

        Output:
        - df: DataFrame with all NaN values filled.
        """
        for col in FLAG_COLS:
            if col in df.columns:
                df[col] = df[col].fillna(-1)
        df = df.fillna(0)
        return df

    def resolve_compound(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluates string-encoded arithmetic expressions in object-type columns.

        Inputs:
        - df: DataFrame potentially containing string arithmetic in object columns.

        Output:
        - df: DataFrame with all compound string values resolved to numeric.
        """
        obj_cols = [c for c in df.select_dtypes(include=["object", "str"]).columns]
        for col in obj_cols:
            df[col] = df[col].apply(self.safe_eval)
        return df

    def safe_eval(self, v) -> object:
        """
        Evaluates a string arithmetic expression if it contains an operator,
        returning the original value unchanged if evaluation fails or is not needed.

        Inputs:
        - v: Value to evaluate, expected to be a string or a non-string scalar.

        Output:
        - result: Evaluated numeric result or the original value.
        """
        if not isinstance(v, str):
            return v
        if not any(op in v for op in ('+', '-', '*', '/')):
            return v
        try:
            return pd.eval(str(v))
        except Exception:
            return v

    def ohe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies One-Hot Encoding to FLAG_COLS present in the DataFrame, then
        reindexes to the training OHE column layout, filling any missing columns with 0.

        Inputs:
        - df: DataFrame containing flag/categorical columns to encode.

        Output:
        - df: DataFrame aligned to the exact feature space used during training.
        """
        present_flag_cols = [c for c in FLAG_COLS if c in df.columns]
        for col in present_flag_cols:
            df[col] = df[col].astype(str)
        df = pd.get_dummies(df, columns=present_flag_cols)
        df = df.reindex(columns=self.ohe_columns, fill_value=0)
        return df

    def scale(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies MinMax scaling using the training scaler to the numeric columns.

        Inputs:
        - df: OHE-encoded DataFrame with numeric columns to scale.

        Output:
        - df: DataFrame with scaled numeric columns.
        """
        present_scale_cols = [c for c in self.scaler_columns if c in df.columns]
        df[present_scale_cols] = df[present_scale_cols].astype(float)
        df[present_scale_cols] = self.scaler.transform(df[present_scale_cols])
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs the full preprocessing pipeline: fill missing values, resolve compound
        expressions, apply OHE, and apply MinMax scaling.

        Inputs:
        - df: Raw single-row packet DataFrame from LiveCapture.

        Output:
        - df: Fully preprocessed DataFrame ready for model inference.
        """
        df = df.copy()
        df = self.fill_missing(df)
        df = self.resolve_compound(df)
        df = self.ohe(df)
        df = self.scale(df)
        return df


# =====================================
# ---       Utility Functions       ---
# =====================================

def get_interface_ip(interface_name: str) -> str:
    """
    Returns the IPv4 address of a given network interface.

    Inputs:
    - interface_name: Name of the network interface to query.

    Output:
    - address: IPv4 address string, or None if the interface has no IPv4 address.
    """
    addresses = psutil.net_if_addrs()
    if interface_name in addresses:
        for addr in addresses[interface_name]:
            if addr.family == socket.AF_INET:
                return addr.address
    return None


# =====================================
# ---            Firewall           ---
# =====================================

class Firewall:
    """
    Core firewall engine: loads the model, starts live capture, runs inference
    on batched packets, and enforces IP blocking rules.

    Inputs:
    - model_path: Path to the saved model joblib file.
    - interface: Network interface name to capture traffic from.
    - bpf_filter: Optional BPF filter string to restrict captured traffic.
    - block: Whether to actively block IPs via OS firewall rules.
    - batch_size: Number of packets to process per inference call.
    - keylog_file: Optional path to a TLS keylog file for decryption.
    """

    def __init__(
            self,
            model_path: str = MODEL_PATH,
            interface: str = "eth0",
            bpf_filter: str = None,
            block: bool = False,
            batch_size: int = 8,
            keylog_file: str = None,
    ):
        self.block = block
        self.batch_size = batch_size
        self.blocked_ips: set = set()

        model = os.path.basename(model_path.removesuffix(".joblib"))
        print(f"[Firewall] Loading model...")
        checkpoint = joblib.load(model_path)
        print(f"[Firewall] Loaded model [{model}]!")
        self.model = checkpoint["model"]
        self.encoder = checkpoint["encoder"]
        self.label_names: list = list(self.encoder.classes_)

        saved_scaler = None
        if os.path.exists(SCALER_PATH):
            try:
                saved_scaler = joblib.load(SCALER_PATH)
                print(f"[Firewall] Loaded training scaler from {SCALER_PATH}")
            except Exception as e:
                print(f"[Firewall] Could not load scaler: {e} — will use warmup instead")

        self.preprocessor = LivePreprocessor(saved_scaler=saved_scaler)

        machine_ip = get_interface_ip(interface)
        if machine_ip:
            bpf = f"dst host {machine_ip} or dst host 127.0.0.1 or dst host ::1"
            if bpf_filter:
                bpf = f"({bpf_filter}) and ({bpf})"
        else:
            bpf = bpf_filter

        self.capture = LiveCapture(
            interface=interface,
            bpf_filter=bpf,
            keylog_file=keylog_file,
        )

        self.stats = {name: 0 for name in self.label_names}
        self.stats["total"] = 0
        self.start_time = time.time()

        self.ddos_strikes = defaultdict(deque)


    # =====================================
    # ---   Firewall Helper Functions   ---
    # =====================================

    def predict(self, df: pd.DataFrame) -> list:
        """
        Preprocesses a batch DataFrame and runs model inference.

        Inputs:
        - df: Raw batch DataFrame containing one or more packet rows.

        Output:
        - labels: List of predicted label strings, one per row.
        """
        try:
            processed = self.preprocessor.preprocess(df)
            X = processed.values.astype(float)
            indices = self.model.predict(X)
            return [self.label_names[i] for i in indices]
        except Exception as e:
            print(f"[Firewall] Prediction error: {e}")
            return ["Unknown"] * len(df)

    def should_block_ip(self, ip: str, label: str) -> bool:
        """
        Determines whether a source IP should be blocked based on the predicted
        label and its recent strike count within the rolling time window.

        Inputs:
        - ip: Source IP address to evaluate.
        - label: Predicted attack label for the current packet.

        Output:
        - should_block: True if the IP meets the blocking threshold.
        """
        if ip in self.blocked_ips:
            return False
        if label in TO_BLOCK_IMMEDIATELY:
            return True
        if label in TO_BLOCK_AFTER_N_INSTANCES:
            now = time.time()
            dq = self.ddos_strikes[ip]
            dq.append(now)
            cutoff = now - DDOS_WINDOW_SECONDS
            while dq and dq[0] < cutoff:
                dq.popleft()
            return len(dq) >= DDOS_STRIKES_TO_BLOCK
        return False

    def should_unblock_ip(self, ip: str) -> bool:
        """
        Determines whether a blocked IP is eligible for automatic unblocking
        based on inactivity since its last recorded strike.

        Inputs:
        - ip: Blocked IP address to evaluate.

        Output:
        - should_unblock: True if the IP has been inactive for more than 300 seconds.
        """
        if ip not in self.blocked_ips:
            return False
        ip_timestamps = self.ddos_strikes[ip]
        if not ip_timestamps:
            return False
        last_ip_timestamp = ip_timestamps[-1]
        return (time.time() - last_ip_timestamp) > 300

    def handle_prediction(self, label: str, source_ip: str) -> None:
        """
        Processes a single prediction result: updates stats, logs the outcome,
        and triggers blocking if the IP meets the threshold.

        Inputs:
        - label: Predicted class label for the packet.
        - source_ip: Source IP address of the packet.
        """
        self.stats[label] = self.stats.get(label, 0) + 1

        if label in TO_BLOCK_IMMEDIATELY or label in TO_BLOCK_AFTER_N_INSTANCES:
            print(f"[WARNING] ⚠  Attack detected: {label:<25} |\tsrc== {source_ip or 'unknown'}")
            if self.should_block_ip(source_ip, label):
                success = self.block_ip(source_ip)
                if not success:
                    print(f"[Firewall] BLOCK FAILED for {source_ip} — check sudo permissions")
        else:
            print(f"[ALLOW] ✓  Normal traffic from {source_ip or 'unknown':<25} | label={label}")

    def block_ip(self, ip: str) -> bool:
        """
        Adds a firewall rule to block all inbound traffic from the given IP
        using the appropriate OS-level command.

        Inputs:
        - ip: IP address to block.

        Output:
        - success: True if the OS command succeeded, False otherwise.
        """
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.run(
                    ["sudo", "pfctl", "-t", "blackwall_blocked", "-T", "add", ip],
                    check=True, capture_output=True
                )
            elif system == "Linux":
                subprocess.run(
                    ["sudo", "iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"],
                    check=True, capture_output=True
                )
            elif system == "Windows":
                subprocess.run(
                    ["netsh", "advfirewall", "firewall", "add", "rule",
                     f"name=Blackwall_Block_{ip}", "dir=in", "action=block",
                     f"remoteip={ip}"],
                    check=True, capture_output=True
                )
            self.blocked_ips.add(ip)
            print(f"[Firewall] Blocked {ip} ({system})")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[Firewall] Failed to block {ip} (sudo/permissions error?): {e.stderr.decode() if e.stderr else e}")
            return False

    def unblock_ip(self, ip: str) -> bool:
        """
        Removes the firewall rule blocking the given IP using the appropriate
        OS-level command and discards it from the internal blocked set on success.

        Inputs:
        - ip: IP address to unblock.

        Output:
        - success: True if the OS command succeeded, False otherwise.
        """
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.run(
                    ["sudo", "pfctl", "-t", "blackwall_blocked", "-T", "delete", ip],
                    check=True, capture_output=True
                )
            elif system == "Linux":
                subprocess.run(
                    ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
                    check=True, capture_output=True
                )
            elif system == "Windows":
                subprocess.run(
                    ["netsh", "advfirewall", "firewall", "delete", "rule",
                     f"name=Blackwall_Block_{ip}"],
                    check=True, capture_output=True
                )
            self.blocked_ips.discard(ip)
            print(f"[Firewall] Unblocked {ip}!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[Firewall] Failed to unblock {ip}: {e.stderr.decode() if e.stderr else e}")
            return False

    def print_stats(self) -> None:
        """
        Prints a summary of classification statistics and currently blocked IPs
        to standard output.
        """
        elapsed = time.time() - self.start_time
        total = self.stats["total"]
        pps = total / elapsed if elapsed > 0 else 0
        print(f"\n--- Stats ({elapsed:.0f}s | {total} pkts | {pps:.1f} pkt/s) ---")
        for name in self.label_names:
            count = self.stats.get(name, 0)
            pct = 100 * count / total if total else 0
            print(f"  {name:<22} {count:>6}  ({pct:.1f}%)")
        print("\n--- Currently blocked ips ---")
        if self.blocked_ips is not None and len(self.blocked_ips) > 0:
            for ip in self.blocked_ips:
                print(f" {ip}")
        else:
            print(" None")
        print()


    # =====================================
    # ---     Main Firewall Pipeline    ---
    # =====================================

    def run(self) -> None:
        """
        Starts live capture and runs the classification loop, processing packets
        in batches until a KeyboardInterrupt is received.
        """
        self.capture.start()
        print("[Firewall] Classification started — training scaler loaded, no warmup needed.")

        try:
            while not self.capture.stop_event.is_set():
                try:
                    source_ip, raw_df = self.capture.queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                batch_ips = [source_ip]
                batch_dfs = [raw_df]

                for _ in range(self.batch_size - 1):
                    try:
                        source_ip, raw_df = self.capture.queue.get_nowait()
                        batch_ips.append(source_ip)
                        batch_dfs.append(raw_df)
                    except queue.Empty:
                        break

                combined = pd.concat(batch_dfs, ignore_index=True)
                labels = self.predict(combined)
                for i, label in enumerate(labels):
                    self.stats["total"] += 1
                    self.handle_prediction(label, batch_ips[i])

                for ip in list(self.blocked_ips):
                    if self.should_unblock_ip(ip):
                        self.unblock_ip(ip)

        except KeyboardInterrupt:
            print("\n[Firewall] Shutting down...")
            self.capture.stop()


# =====================================
# ---       Main Execution          ---
# =====================================

if __name__ == "__main__":
    fire = Firewall(
        model_path=MODEL_PATH,
        interface="en0",
        bpf_filter=None,
        block=False,
        batch_size=8,
        keylog_file=None,
    )
    fire.run()