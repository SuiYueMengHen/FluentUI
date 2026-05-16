from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGridLayout, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             PrimaryPushButton, PushButton, ToolButton, ToggleButton,
                             RadioButton, CheckBox, ProgressBar, InfoBadge,
                             DotInfoBadge, CaptionLabel, FluentIcon as FIF,
                             HyperlinkLabel, SwitchButton)

from app.theme_aware_page import ThemeAwarePage


class BasicWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("basicWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Basic Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Essential UI components for building modern desktop applications.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_buttons_section(main_layout)
        self._build_labels_section(main_layout)
        self._build_progress_section(main_layout)
        self._build_badges_section(main_layout)
        self._build_switches_section(main_layout)

        main_layout.addStretch()

    def _build_buttons_section(self, parent):
        group = QGroupBox("Buttons")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(16)

        row1 = QHBoxLayout()
        row1.setSpacing(12)
        row1.addWidget(PrimaryPushButton("Primary Button"))
        row1.addWidget(PushButton("Standard Button"))
        row1.addWidget(ToolButton(FIF.SETTING))
        row1.addStretch()
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(12)
        toggle = ToggleButton("Toggle Button")
        toggle.setChecked(True)
        row2.addWidget(toggle)
        disabled_btn = PushButton("Disabled Button")
        disabled_btn.setEnabled(False)
        row2.addWidget(disabled_btn)
        row2.addStretch()
        layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.setSpacing(20)
        for text in ["Option A", "Option B", "Option C"]:
            rb = RadioButton(text)
            if text == "Option A":
                rb.setChecked(True)
            row3.addWidget(rb)
        row3.addStretch()
        layout.addLayout(row3)

        row4 = QHBoxLayout()
        row4.setSpacing(20)
        for text in ["Accept Terms", "Remember Me", "Newsletter"]:
            cb = CheckBox(text)
            if text == "Accept Terms":
                cb.setChecked(True)
            row4.addWidget(cb)
        row4.addStretch()
        layout.addLayout(row4)

        parent.addWidget(group)

    def _build_labels_section(self, parent):
        group = QGroupBox("Labels & Typography")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        layout.addWidget(TitleLabel("Title Label — 28px Bold"))
        layout.addWidget(SubtitleLabel("Subtitle Label — 20px SemiBold"))
        layout.addWidget(BodyLabel("Body Label — 14px Regular. This is the default text style for most content."))
        layout.addWidget(CaptionLabel("Caption Label — 12px. Used for secondary information and metadata."))
        layout.addWidget(HyperlinkLabel("https://qfluentwidgets.com"))

        parent.addWidget(group)

    def _build_progress_section(self, parent):
        group = QGroupBox("Progress Indicators")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(16)

        layout.addWidget(BodyLabel("Determinate Progress:"))
        bar1 = ProgressBar()
        bar1.setValue(65)
        layout.addWidget(bar1)

        layout.addWidget(BodyLabel("Indeterminate Progress:"))
        bar2 = ProgressBar()
        bar2.setRange(0, 0)
        layout.addWidget(bar2)

        parent.addWidget(group)

    def _build_badges_section(self, parent):
        group = QGroupBox("Badges")
        self._track_group(group)
        layout = QHBoxLayout(group)
        layout.setSpacing(24)

        layout.addWidget(InfoBadge.info("Info"))
        layout.addWidget(InfoBadge.success("Success"))
        layout.addWidget(InfoBadge.warning("Warning"))
        layout.addWidget(InfoBadge.error("Error"))
        layout.addWidget(DotInfoBadge())
        layout.addStretch()

        parent.addWidget(group)

    def _build_switches_section(self, parent):
        group = QGroupBox("Switches")
        self._track_group(group)
        layout = QHBoxLayout(group)
        layout.setSpacing(24)

        sw1 = SwitchButton("Wi-Fi")
        sw1.setChecked(True)
        layout.addWidget(sw1)

        sw2 = SwitchButton("Bluetooth")
        layout.addWidget(sw2)

        sw3 = SwitchButton("Dark Mode")
        sw3.setChecked(True)
        layout.addWidget(sw3)

        layout.addStretch()
        parent.addWidget(group)
