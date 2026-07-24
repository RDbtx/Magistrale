import queue


# =====================================
# ---         Event Bus             ---
# =====================================

class GUIEventBus:
    """
    Thread-safe event bus that decouples the firewall engine from the GUI.
    The firewall thread posts events; the GUI poll loop drains and renders them.
    """

    LOG   = "log"
    ROW   = "row"
    STAT  = "stat"
    STATS = "stats_panel"
    BLOCK = "blocked_ips"

    def __init__(self):
        self.q: queue.Queue = queue.Queue()


    # =====================================
    # ---       Posting Functions       ---
    # =====================================

    def post(self, payload: dict) -> None:
        """
        Places a raw event payload on the internal queue.

        Inputs:
        - payload: Dictionary representing the event, must include a 'type' key.
        """
        self.q.put_nowait(payload)

    def post_log(self, msg: str, level: str = "info") -> None:
        """
        Posts a log message event.

        Inputs:
        - msg: Log message text.
        - level: Severity level of the message.
        """
        self.post({"type": self.LOG, "msg": msg, "level": level})

    def post_row(self, ts: str, action: str, ip: str, label: str) -> None:
        """
        Posts a traffic table row event representing a single classified packet.

        Inputs:
        - ts: Timestamp string for the packet.
        - action: Disposition string, either 'ALLOW' or 'WARNING'.
        - ip: Source IP address of the packet.
        - label: Predicted class label for the packet.
        """
        self.post({"type": self.ROW, "ts": ts, "action": action, "ip": ip, "label": label})

    def post_stat(self, allowed: int, warnings: int, total: int) -> None:
        """
        Posts a counter update event for the top-bar stat cards.

        Inputs:
        - allowed: Cumulative count of allowed packets.
        - warnings: Cumulative count of warning packets.
        - total: Cumulative count of all packets processed.
        """
        self.post({"type": self.STAT, "allowed": allowed, "blocked": warnings, "total": total})

    def post_stats_panel(self, elapsed: float, total: int, pps: float,
                         label_counts: dict, label_names: list) -> None:
        """
        Posts a full classification stats update event for the stats panel.

        Inputs:
        - elapsed: Seconds since the firewall started.
        - total: Total number of packets processed.
        - pps: Current packets-per-second throughput.
        - label_counts: Dictionary mapping each label name to its packet count.
        - label_names: Ordered list of all label name strings.
        """
        self.post({
            "type": self.STATS,
            "elapsed": elapsed, "total": total, "pps": pps,
            "label_counts": label_counts,
            "label_names": label_names,
        })

    def post_blocked_ips(self, ips: set) -> None:
        """
        Posts the current set of blocked IP addresses.

        Inputs:
        - ips: Set of IP address strings currently blocked by the firewall.
        """
        self.post({"type": self.BLOCK, "ips": set(ips)})


    # =====================================
    # ---       Draining Function       ---
    # =====================================

    def drain(self) -> list:
        """
        Removes and returns all currently queued events without blocking.

        Output:
        - items: List of all event payload dictionaries available in the queue.
        """
        items = []
        try:
            while True:
                items.append(self.q.get_nowait())
        except queue.Empty:
            pass
        return items