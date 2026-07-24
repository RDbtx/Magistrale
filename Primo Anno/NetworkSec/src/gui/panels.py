from datetime import datetime
import flet as ft

from src.gui.theme import (
    ACCENT, BG, BORDER, CELL_BG, DANGER, FONT,
    HEADER_BG, HEADER_FG, PANEL2, SUCCESS, SZ,
    TEXT, TEXT_DIM, TEXT_MUTED,
)


# =====================================
# ---       Widget Helpers          ---
# =====================================

def text_ui(text: str, color: str = TEXT, size: int = SZ, weight=None) -> ft.Text:
    """
    Creates a styled Flet Text widget using the application font.

    Inputs:
    - text: Text content to display.
    - color: Hex colour string for the text.
    - size: Font size in points.
    - weight: Optional Flet FontWeight value.

    Output:
    - widget: Configured ft.Text instance.

    """
    kwargs = dict(color=color, size=size, weight=weight)
    if FONT:
        kwargs["font_family"] = FONT
    return ft.Text(text, **kwargs)


def label_text(text: str, color: str = TEXT_DIM, size: int = SZ - 1) -> ft.Text:
    """
    Creates a small uppercased bold label widget, used for field captions.

    Inputs:
    - text: Label content, automatically uppercased.
    - color: Hex colour string for the label.
    - size: Font size in points.

    Output:
    - widget: Configured ft.Text instance.

    """
    return ft.Text(
        text.upper(),
        font_family=FONT,
        color=color,
        size=size,
        weight=ft.FontWeight.BOLD,
    )


def panel_header(title: str, icon: str = "▓▓", trailing=None) -> ft.Container:
    """
    Builds a panel header bar with an icon badge, title, and optional trailing widget.

    Inputs:
    - title: Header title text, automatically uppercased.
    - icon: Icon string displayed in the badge on the left.
    - trailing: Optional Flet control appended to the right of the header.

    Output:
    - header: Configured ft.Container instance.

    """
    row_items = [
        ft.Container(
            content=ft.Text(icon, color=HEADER_BG, size=9, font_family=FONT),
            bgcolor=HEADER_FG,
            width=22,
            height=22,
        ),
        ft.Text(
            title.upper(),
            font_family=FONT,
            color=HEADER_FG,
            size=SZ,
            weight=ft.FontWeight.BOLD,
        ),
        ft.Container(expand=True, height=1, bgcolor=HEADER_FG + "55"),
    ]
    if trailing is not None:
        row_items.append(trailing)
    return ft.Container(
        content=ft.Row(row_items, spacing=6,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=HEADER_BG,
        padding=ft.Padding.symmetric(horizontal=8, vertical=5),
    )


def panel(title: str, body, expand: int, icon: str = "▓▓", trailing=None) -> ft.Container:
    """
    Wraps a body widget in a standard bordered panel with a header bar.

    Inputs:
    - title: Panel title displayed in the header.
    - body: Flet control placed in the panel body.
    - expand: Flex expand factor for the panel within its parent row.
    - icon: Icon string displayed in the header badge.
    - trailing: Optional Flet control appended to the right of the header.

    Output:
    - container: Configured ft.Container panel instance.

    """
    return ft.Container(
        expand=expand,
        bgcolor=CELL_BG,
        border=ft.Border.all(1, BORDER),
        border_radius=0,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column(
            [
                panel_header(title, icon, trailing=trailing),
                ft.Container(content=body, expand=True),
            ],
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )


def ydiv() -> ft.Container:
    """
    Returns a thin horizontal divider line.

    Output:
    - divider: ft.Container styled as a horizontal rule.

    """
    return ft.Container(height=1, bgcolor=BORDER + "88")


def vscroll(content, pad: int = 0) -> ft.ListView:
    """
    Wraps a widget in a vertically scrollable ListView.

    Inputs:
    - content: Flet control to make scrollable.
    - pad: Padding in points applied around the content.

    Output:
    - scroll_view: ft.ListView containing the content.

    """
    return ft.ListView(
        controls=[ft.Container(content=content, padding=pad)],
        expand=True, spacing=0, padding=0, auto_scroll=False,
    )


def hvscroll(content, pad: int = 0) -> ft.Column:
    """
    Wraps a widget in a vertically and horizontally scrollable container.
    Used for panels such as the log and blocked IPs list.

    Inputs:
    - content: Flet control to make scrollable.
    - pad: Padding in points applied around the content.

    Output:
    - scroll_view: ft.Column with both vertical and horizontal scroll enabled.

    """
    return ft.Column(
        controls=[
            ft.Row(
                controls=[ft.Container(content=content, padding=pad)],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        ],
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )


def stat_card(title: str, widget, accent: str) -> ft.Container:
    """
    Builds a small stat display card with a label and a value widget.

    Inputs:
    - title: Caption text displayed above the value.
    - widget: Flet control displaying the stat value.
    - accent: Hex colour string used for the card border.

    Output:
    - card: Configured ft.Container instance.

    """
    return ft.Container(
        content=ft.Column(
            [label_text(title), widget],
            spacing=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=PANEL2,
        border=ft.Border.all(1, accent),
        padding=ft.Padding.symmetric(horizontal=14, vertical=6),
    )


# =====================================
# ---         System Log Panel      ---
# =====================================

class LogPanel:
    """
    Owns the system-log column and exposes push() to append timestamped entries.
    Automatically trims entries when the maximum capacity is exceeded.

    """

    MAX_ENTRIES = 400

    def __init__(self):
        self.log_col = ft.Column(spacing=1)
        self.control = panel("SYSTEM LOG", hvscroll(self.log_col, pad=8),
                             expand=3, icon="▓▓")

    def clear(self) -> None:
        """
        Removes all entries from the log column.
        """
        self.log_col.controls.clear()

    def push(self, msg: str, level: str = "info") -> None:
        """
        Appends a new timestamped log entry to the column.

        Inputs:
        - msg: Log message text to display.
        - level: Severity level, used to set the text colour.

        """
        color = DANGER if level == "danger" else TEXT
        self.log_col.controls.append(
            ft.Row(
                spacing=5,
                controls=[
                    text_ui(datetime.now().strftime("%H:%M:%S"), TEXT_DIM, SZ - 3),
                    ft.Container(
                        content=text_ui(">>", color, SZ - 3, ft.FontWeight.BOLD),
                        bgcolor=BG,
                        padding=ft.Padding.symmetric(horizontal=3, vertical=1),
                    ),
                    ft.Text(msg.strip(), font_family=FONT,
                            size=SZ - 3, color=color, no_wrap=True),
                ],
            )
        )
        if len(self.log_col.controls) > self.MAX_ENTRIES:
            self.log_col.controls.pop(0)


def build_log_panel() -> tuple:
    """
    Instantiates the LogPanel and returns its public interface.

    Outputs:
    - control: The panel's root Flet container.
    - push_fn: Function to append a new log entry.
    - clear_fn: Function to clear all log entries.

    """
    lp = LogPanel()
    return lp.control, lp.push, lp.clear


# =====================================
# ---     Live Traffic Matrix Panel  -
# =====================================

def make_traffic_column(label: str) -> ft.DataColumn:
    """
    Creates a styled DataTable column header.

    Inputs:
    - label: Column header text.

    Output:
    - column: Configured ft.DataColumn instance.

    """
    return ft.DataColumn(
        ft.Text(label, color=ACCENT, size=SZ,
                font_family=FONT, weight=ft.FontWeight.BOLD)
    )


class TrafficPanel:
    """
    Owns the live-traffic DataTable and exposes push_row() and clear().
    Only WARNING-level rows are displayed; ALLOW rows are silently discarded.
    """

    MAX_ROWS = 200

    def __init__(self):
        self.table = ft.DataTable(
            columns=[
                make_traffic_column("TIME"),
                make_traffic_column("ACTION"),
                make_traffic_column("IP ADDRESS"),
                make_traffic_column("LABEL"),
            ],
            rows=[],
            border=ft.Border.all(1, BORDER + "55"),
            heading_row_color={"": "#0d1a09"},
            heading_row_height=26,
            data_row_min_height=22,
            data_row_max_height=22,
            divider_thickness=0,
            column_spacing=10,
        )
        wrap = ft.Container(content=self.table, expand=True,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE)
        self.control = panel("THREAT TRAFFIC MATRIX", vscroll(wrap, pad=8),
                             expand=5, icon="▓▓")

    def push_row(self, ts: str, action: str, ip: str, label: str) -> None:
        """
        Inserts a new row at the top of the traffic table if the action is a WARNING.

        Inputs:
        - ts: Timestamp string for the packet.
        - action: Disposition string; only 'WARNING' rows are inserted.
        - ip: Source IP address of the packet.
        - label: Predicted class label for the packet.

        """
        if action != "WARNING":
            return
        self.table.rows.insert(
            0,
            ft.DataRow(cells=[
                ft.DataCell(text_ui(ts, TEXT_DIM, SZ)),
                ft.DataCell(text_ui(action, DANGER, SZ, ft.FontWeight.BOLD)),
                ft.DataCell(text_ui(ip, TEXT, SZ)),
                ft.DataCell(text_ui(label, DANGER, SZ)),
            ]),
        )
        if len(self.table.rows) > self.MAX_ROWS:
            self.table.rows.pop()

    def clear(self) -> None:
        """
        Removes all rows from the traffic table.
        """
        self.table.rows.clear()


def build_traffic_panel() -> tuple:
    """
    Instantiates the TrafficPanel and returns its public interface.

    Outputs:
    - control: The panel's root Flet container.
    - push_row_fn: Function to insert a new traffic row.
    - clear_fn: Function to clear all traffic rows.
    """
    tp = TrafficPanel()
    return tp.control, tp.push_row, tp.clear


# =====================================
# ---   Classification Stats Panel  ---
# =====================================

class StatsPanel:
    """
    Owns the classification stats column and exposes update() and clear().
    Displays per-label packet counts, percentages, and bar indicators.
    """

    NAME_W  = 170
    COUNT_W = 55
    PCT_W   = 70

    def __init__(self):
        self.meta_pkt = text_ui("--", TEXT_DIM, SZ)
        self.meta_pkt.width = 70
        self.meta_pps = text_ui("--", TEXT_DIM, SZ)
        self.meta_pps.width = 70
        self.meta_up = text_ui("--", TEXT_DIM, SZ)
        self.meta_up.width = 70

        meta_row = ft.Row(controls=[self.meta_pkt, self.meta_pps, self.meta_up], spacing=16)
        self.rows_col = ft.Column(spacing=3)

        body = ft.Column(
            [meta_row, ydiv(), self.rows_col],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        self.control = panel("CLASSIFICATION STATS", vscroll(body, pad=8),
                             expand=3, icon="◈◈")

    def update(self, elapsed: float, total: int, pps: float,
               label_counts: dict, label_names: list) -> None:
        """
        Refreshes the metadata row and rebuilds all per-label stat rows.

        Inputs:
        - elapsed: Seconds since the firewall started.
        - total: Total number of packets processed.
        - pps: Current packets-per-second throughput.
        - label_counts: Dictionary mapping each label name to its packet count.
        - label_names: Ordered list of all label name strings.
        """
        self.meta_pkt.value = f"PKT {total}"
        self.meta_pps.value = f"pkt/s {pps:.1f}"
        self.meta_up.value = f"UP {elapsed:.0f} s"
        self.rows_col.controls.clear()

        names = list(label_names)
        normal = [n for n in names if n.lower() == "normal"]
        others = sorted(
            [n for n in names if n.lower() != "normal"],
            key=lambda n: label_counts.get(n, 0),
            reverse=True,
        )
        for name in normal + others:
            count = label_counts.get(name, 0)
            pct = 100 * count / total if total else 0.0
            bar_w = max(1, int(pct * 1.2))
            self.rows_col.controls.append(
                ft.Column([
                    ft.Row([
                        ft.Container(width=self.NAME_W,
                                     content=text_ui(name, TEXT, SZ)),
                        ft.Container(width=self.COUNT_W,
                                     alignment=ft.Alignment.CENTER_RIGHT,
                                     content=text_ui(str(count), TEXT, SZ,
                                                     ft.FontWeight.BOLD)),
                        ft.Container(width=self.PCT_W,
                                     alignment=ft.Alignment.CENTER_RIGHT,
                                     content=text_ui(f"{pct:.1f}%", TEXT_DIM, SZ)),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Container(
                        content=ft.Container(width=bar_w, height=2, bgcolor=ACCENT),
                        bgcolor=TEXT_MUTED, height=2, expand=True,
                    ),
                ], spacing=1)
            )

    def clear(self) -> None:
        """
        Removes all per-label rows from the stats column.
        """
        self.rows_col.controls.clear()


def build_stats_panel() -> tuple:
    """
    Instantiates the StatsPanel and returns its public interface.

    Outputs:
    - control: The panel's root Flet container.
    - update_fn: Function to refresh the stats display.
    - clear_fn: Function to clear all stat rows.
    """
    sp = StatsPanel()
    return sp.control, sp.update, sp.clear


# =====================================
# ---       Blocked IPs Panel       ---
# =====================================

class BlockedPanel:
    """
    Owns the blocked-IP list, badge counter, and manual-unblock input field.

    Inputs:
    - fw_ref: Single-element list holding the active GUIFirewall instance or None.
    - bus_ref: Single-element list holding the active GUIEventBus instance or None.
    - push_log: Callable used to post messages to the system log panel.
    - page: Active Flet page instance, required to trigger UI updates.
    """

    def __init__(self, fw_ref: list, bus_ref: list, push_log, page: ft.Page):
        self.fw_ref = fw_ref
        self.bus_ref = bus_ref
        self.push_log = push_log
        self.page = page

        self.badge = ft.Container(
            content=ft.Text("0", font_family=FONT, color=HEADER_FG,
                            size=SZ, weight=ft.FontWeight.BOLD),
            bgcolor=HEADER_FG + "22",
            border=ft.Border.all(1, HEADER_FG),
            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
            margin=ft.Margin(right=4, left=0, top=0, bottom=0),
        )

        self.blocked_col = ft.Column(spacing=4)

        self.unblock_input = ft.TextField(
            hint_text="IP address...",
            hint_style=ft.TextStyle(font_family=FONT, color=TEXT_MUTED, size=SZ),
            text_style=ft.TextStyle(font_family=FONT, color=TEXT, size=SZ),
            bgcolor=BG,
            border_color=BORDER,
            focused_border_color=BORDER,
            border_radius=0,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=6),
            expand=True,
            height=32,
        )

        unblock_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=DANGER,
            icon_size=16,
            on_click=self.on_manual_unblock,
            tooltip="Unblock IP",
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: BG,
                         ft.ControlState.HOVERED: "#2a0810"},
                shape=ft.RoundedRectangleBorder(radius=0),
                side=ft.BorderSide(1, DANGER),
                padding=ft.Padding.all(4),
            ),
        )

        unblock_section = ft.Container(
            content=ft.Column([
                ft.Container(height=1, bgcolor=BORDER),
                ft.Container(
                    content=ft.Column([
                        label_text("MANUAL UNBLOCK"),
                        ft.Row([self.unblock_input, unblock_btn], spacing=4),
                    ], spacing=4),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=6),
                ),
            ], spacing=0),
            bgcolor=PANEL2,
        )

        self.control = ft.Container(
            expand=2,
            bgcolor=CELL_BG,
            border=ft.Border.all(1, BORDER),
            border_radius=0,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Column(
                [
                    panel_header("BLOCKED IPs", "██", trailing=self.badge),
                    ft.Container(content=hvscroll(self.blocked_col, pad=8), expand=True),
                    unblock_section,
                ],
                spacing=0, expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        )

        self.update(set())

    def do_unblock(self, ip: str) -> bool:
        """
        Performs the unblock operation on the active firewall and posts a bus event.

        Inputs:
        - ip: IP address to unblock.

        Output:
        - success: True if the unblock succeeded, False otherwise.
        """
        fw = self.fw_ref[0]
        if not fw:
            self.push_log(f"[Firewall] No active session to unblock {ip}", "warn")
            return False
        if ip not in fw.blocked_ips:
            self.push_log(f"[Firewall] {ip} is not in the blocked list", "warn")
            return False
        success = fw.unblock_ip(ip)
        if success:
            self.push_log(f"[Firewall] Unblocked {ip}", "info")
            bus = self.bus_ref[0]
            if bus:
                bus.post_blocked_ips(fw.blocked_ips)
        else:
            self.push_log(f"[Firewall] FAILED to unblock {ip} (check sudo)", "danger")
        return success

    def on_ip_unblock_click(self, ip: str) -> None:
        """
        Click handler for the unblock button next to each listed IP.

        Inputs:
        - ip: IP address to unblock.
        """
        self.do_unblock(ip)
        self.page.update()

    def on_manual_unblock(self, _) -> None:
        """
        Click handler for the manual-unblock text field submit button.
        Reads the IP from the input field, attempts to unblock it, then clears the field.
        """
        ip = (self.unblock_input.value or "").strip()
        if ip:
            self.do_unblock(ip)
        self.unblock_input.value = ""
        self.page.update()

    def update(self, ips: set) -> None:
        """
        Rebuilds the blocked IP list display from the provided set.

        Inputs:
        - ips: Current set of blocked IP address strings.
        """
        self.badge.content.value = str(len(ips))
        self.blocked_col.controls.clear()

        if not ips:
            self.blocked_col.controls.append(
                ft.Row([
                    ft.Container(width=4, height=4, bgcolor=TEXT_MUTED),
                    text_ui("none", TEXT_MUTED, SZ),
                ], spacing=8)
            )
        else:
            for ip in sorted(ips):
                self.blocked_col.controls.append(self.make_ip_row(ip))

    def make_ip_row(self, ip: str) -> ft.Row:
        """
        Builds a single row widget displaying a blocked IP with an unblock button.

        Inputs:
        - ip: IP address string to display.

        Output:
        - row: Configured ft.Row widget for the given IP.
        """
        return ft.Row(
            [
                ft.Container(width=6, height=6, bgcolor=DANGER),
                text_ui(ip, DANGER, SZ),
                ft.Container(expand=True),
                ft.TextButton(
                    "✕",
                    on_click=lambda _, target=ip: self.on_ip_unblock_click(target),
                    style=ft.ButtonStyle(
                        color={ft.ControlState.DEFAULT: TEXT_MUTED,
                               ft.ControlState.HOVERED: DANGER},
                        padding=ft.Padding.all(0),
                    ),
                ),
            ],
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )


def build_blocked_panel(fw_ref: list, bus_ref: list, push_log, page: ft.Page) -> tuple:
    """
    Instantiates the BlockedPanel and returns its public interface.

    Inputs:
    - fw_ref: Single-element list holding the active GUIFirewall instance or None.
    - bus_ref: Single-element list holding the active GUIEventBus instance or None.
    - push_log: Callable used to post messages to the system log panel.
    - page: Active Flet page instance.

    Outputs:
    - control: The panel's root Flet container.
    - update_fn: Function to refresh the blocked IP list.
    """
    bp = BlockedPanel(fw_ref, bus_ref, push_log, page)
    return bp.control, bp.update