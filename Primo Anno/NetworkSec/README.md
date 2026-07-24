# Blackwall —  An AI-Powered Firewall for Modern HTTP Traffic
 

A ml based firewall that captures traffic with `tshark`, classifies
each packet with a trained ML model, and automatically bans source IPs whose
traffic matches the configured attack rules. It can be run headless (automatic
mode) or through a graphical interface (GUI mode).

---

## Requirements

### Python packages

```bash
pip install pandas
pip install numpy
pip install scikit-learn
pip install lightgbm
pip install xgboost
pip install flet
pip install termcolor
pip install joblib
pip install matplotlib
pip install psutil
```

Or, in one line:

| Package | Used for |
|---|---|
| `pandas`, `numpy` | Packet data frames and numeric processing |
| `scikit-learn` | Label encoding, scaling, train/test split, Random Forest, metrics |
| `lightgbm`, `xgboost` | Alternative gradient-boosting classifiers (training pipeline) |
| `joblib` | Loading/saving the trained model and the fitted scaler |
| `flet` | The desktop GUI |
| `termcolor` | Coloured console output |
| `matplotlib` | Confusion matrices / performance reports |
| `psutil` | Resolving the IPv4 address of the selected interface |

### System dependency: tshark (Wireshark)

Live capture is performed by **`tshark`**, the command-line component of
**Wireshark**. It is *not* a pip package and must be installed separately:

- **macOS:** `brew install wireshark`
- **Debian/Ubuntu:** `sudo apt install tshark`
- **Windows:** install [Wireshark](https://www.wireshark.org/) (includes `tshark.exe`)

The firewall auto-detects `tshark` on `PATH` and in the usual install locations.
If it lives somewhere unusual, point to it with the `TSHARK` environment variable:

```bash
export TSHARK=/path/to/tshark
```

---

## Elevated privileges (required)

The firewall **must be run with elevated privileges** to work properly:

- **Live capture** with `tshark` requires permission to read from a network
  interface in promiscuous mode.
- **IP blocking/unblocking** is enforced through OS-level firewall commands:
  `pfctl` on macOS, `iptables` on Linux, `netsh advfirewall` on Windows; all of
  which need root/administrator rights. Without them, blocking silently fails and
  you will see `BLOCK FAILED … check sudo permissions` in the logs.

Run with `sudo` on macOS/Linux, or from an **Administrator** shell on Windows.

---

## How to use

There are two ways to run the system.

### 1. Automatic mode (headless)

The firewall runs directly from `firewall_engine.py`. Configure it by editing the
parameters in the `if __name__ == "__main__":` block at the bottom of the file:

```python
if __name__ == "__main__":
    fire = Firewall(
        model_path=MODEL_PATH,   # path to the trained model .joblib
        interface="en0",         # interface to monitor (e.g. en0, eth0, Wi-Fi)
        bpf_filter=None,         # optional BPF capture filter, e.g. "tcp port 443"
        block=False,             # set True to actually apply OS firewall rules
        batch_size=8,            # packets per inference batch
        keylog_file=None,        # optional TLS SSLKEYLOGFILE for decryption
    )
    fire.run()
```

Then run it (with elevated privileges):

```bash
sudo python firewall_engine.py
```

It captures live traffic, classifies it in batches, prints `ALLOW` / `WARNING`
lines to the console, automatically blocks offending IPs once they cross the
configured strike threshold, and automatically unblocks IPs that have been
inactive long enough. Stop it with `Ctrl-C`.

### 2. GUI mode

The firewall runs from `main.py`, which launches the graphical interface:

```bash
sudo -v && while true; do sudo -v; sleep 240; done &                                    
python main.py
```

Workflow:

1. **Boot screen:** a startup screen is shown first, then hands off to the main
   interface.
2. **Select interface:** once booted, pick the network interface you want to
   monitor from the **INTERFACE** dropdown (interfaces are discovered via `tshark`).
3. **Start:** press **▶ INITIATE** to launch the firewall engine on the selected
   interface. The status indicator switches to **ONLINE**.
4. **Monitor:** all traffic data is reported live across the panels: a system
   **log**, a per-packet **traffic** feed (timestamp / action / IP / label),
   running **stats** (allowed, warnings, total, packets-per-second, per-label
   counts), and the list of **blocked** IPs.
5. **Automatic banning:** IPs are banned automatically whenever traffic matching
   the patterns defined by the rules is detected.
6. **Manual unban:** you can unban any IP directly from the graphical interface
   via the blocked-IPs panel.
7. **Stop:** press **■ TERMINATE** to stop the engine.

---

## Known limitations

**The core of this project, the packet classifier, sadly does not work well, and relying on
it is ill-advised.** It was trained on a poor-quality dataset, so its predictions
are unreliable: expect both missed attacks and false positives. The capture,
GUI, rule engine, and blocking machinery all function, but the quality of the
detections feeding them is poort at best.