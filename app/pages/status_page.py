from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.step_indicator import StepIndicator
from app.components.battery_indicator import BatteryIndicator
from app.components.signal_strength import SignalStrength
from app.components.connection_status import ConnectionStatus
from app.components.countdown_timer import CountdownTimer
from app.components.circular_progress import CircularProgress
from app.components.linear_timeline import LinearTimeline
from app.components.status_pill import StatusPill


class StatusPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Status", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Status indicators, progress displays, and system state components.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_step_indicator(main_layout)
        self._build_battery_indicator(main_layout)
        self._build_signal_strength(main_layout)
        self._build_connection_status(main_layout)
        self._build_countdown_timer(main_layout)
        self._build_circular_progress(main_layout)
        self._build_linear_timeline(main_layout)
        self._build_status_pill(main_layout)

        main_layout.addStretch()

    def _build_step_indicator(self, parent):
        group = QGroupBox("Step Indicator")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Multi-step progress indicator with animated transitions between steps.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        steps = StepIndicator(
            steps=["Account", "Profile", "Preferences", "Complete"],
            current=2,
        )
        layout.addWidget(steps)
        parent.addWidget(group)

    def _build_battery_indicator(self, parent):
        group = QGroupBox("Battery Indicator")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Battery level indicator with fill animation and color-coded charge states.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        levels = [(85, "High"), (45, "Medium"), (15, "Low")]
        for level, label_text in levels:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            battery = BatteryIndicator(level=level)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(battery, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_signal_strength(self, parent):
        group = QGroupBox("Signal Strength")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Signal strength bars with animated fill for connectivity status display.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        strengths = [(4, "Excellent"), (3, "Good"), (2, "Fair"), (1, "Weak")]
        for strength, label_text in strengths:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            signal = SignalStrength(strength=strength)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(signal, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_connection_status(self, parent):
        group = QGroupBox("Connection Status")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Connection status indicator with pulsing dot for online and static dot for offline.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        connected = ConnectionStatus(connected=True, label="Connected")
        disconnected = ConnectionStatus(connected=False, label="Disconnected")

        row.addWidget(connected)
        row.addWidget(disconnected)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_countdown_timer(self, parent):
        group = QGroupBox("Countdown Timer")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Countdown timer with flip animation and configurable duration.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        timer = CountdownTimer(seconds=300)
        layout.addWidget(timer)
        parent.addWidget(group)

    def _build_circular_progress(self, parent):
        group = QGroupBox("Circular Progress")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Circular progress indicator with arc animation and customizable size and color.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        configs = [
            (25, "#FF6B6B", "25%"),
            (60, "#FFB900", "60%"),
            (90, "#6CCB5F", "90%"),
        ]
        for value, color, label_text in configs:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            progress = CircularProgress(value=value, size=80, stroke_width=6, color=color)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_linear_timeline(self, parent):
        group = QGroupBox("Linear Timeline")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Horizontal timeline with event markers and drawing animation for milestone tracking.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        timeline = LinearTimeline(events=[
            {"label": "Start", "color": "#0078D4"},
            {"label": "Build", "color": "#FFB900"},
            {"label": "Test", "color": "#6CCB5F"},
            {"label": "Deploy", "color": "#0F7B0F"},
        ])
        layout.addWidget(timeline)
        parent.addWidget(group)

    def _build_status_pill(self, parent):
        group = QGroupBox("Status Pill")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Compact status pill with color-coded types for info, success, warning, and error states.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        pill_info = StatusPill(text="Informational", status="info")
        pill_success = StatusPill(text="Completed", status="success")
        pill_warning = StatusPill(text="Pending", status="warning")
        pill_error = StatusPill(text="Failed", status="error")

        row.addWidget(pill_info)
        row.addWidget(pill_success)
        row.addWidget(pill_warning)
        row.addWidget(pill_error)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)
