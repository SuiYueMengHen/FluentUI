from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox)
from PySide6.QtCore import Qt, QTimer
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             InfoBar, InfoBarPosition, PushButton, PrimaryPushButton,
                             MessageBox, StateToolTip, ProgressBar,
                             FluentIcon as FIF, isDarkTheme)

from app.theme_aware_page import ThemeAwarePage


class FeedbackWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("feedbackWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Feedback Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Components for providing user feedback, notifications, and confirmations.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_infobars(main_layout)
        self._build_dialogs(main_layout)
        self._build_progress_demo(main_layout)
        self._build_state_tooltip(main_layout)

        self._state_tooltip = None
        self._progress_timer = None
        self._progress_val = 0
        self._tooltip_update_timer = QTimer(self)
        self._tooltip_update_timer.setSingleShot(True)
        self._tooltip_update_timer.setInterval(3000)
        self._tooltip_update_timer.timeout.connect(self._on_tooltip_update)

        self._tooltip_close_timer = QTimer(self)
        self._tooltip_close_timer.setSingleShot(True)
        self._tooltip_close_timer.setInterval(5000)
        self._tooltip_close_timer.timeout.connect(self._on_tooltip_close)

        main_layout.addStretch()

    def _build_infobars(self, parent):
        group = QGroupBox("Info Bars")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        info_btn = PushButton("Show Info")
        success_btn = PushButton("Show Success")
        warning_btn = PushButton("Show Warning")
        error_btn = PushButton("Show Error")

        info_btn.clicked.connect(lambda: self._show_info_bar("info"))
        success_btn.clicked.connect(lambda: self._show_info_bar("success"))
        warning_btn.clicked.connect(lambda: self._show_info_bar("warning"))
        error_btn.clicked.connect(lambda: self._show_info_bar("error"))

        btn_row.addWidget(info_btn)
        btn_row.addWidget(success_btn)
        btn_row.addWidget(warning_btn)
        btn_row.addWidget(error_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addWidget(BodyLabel("Click the buttons above to see InfoBar notifications at the top of the window."))

        parent.addWidget(group)

    def _show_info_bar(self, level):
        window = self.window()
        bar_func = {
            "info": InfoBar.info,
            "success": InfoBar.success,
            "warning": InfoBar.warning,
            "error": InfoBar.error,
        }
        configs = {
            "info": ("Information", "This is an informational message for the user."),
            "success": ("Success", "Operation completed successfully!"),
            "warning": ("Warning", "Please review the settings before proceeding."),
            "error": ("Error", "Something went wrong. Please try again."),
        }
        title, content = configs[level]
        bar_func[level](title, content, parent=window, position=InfoBarPosition.TOP, duration=3000)

    def _build_dialogs(self, parent):
        group = QGroupBox("Dialogs")
        self._track_group(group)
        layout = QHBoxLayout(group)
        layout.setSpacing(12)

        msg_btn = PushButton("Show MessageBox")
        msg_btn.clicked.connect(self._show_message_box)
        layout.addWidget(msg_btn)

        confirm_btn = PrimaryPushButton("Show Confirm Dialog")
        confirm_btn.clicked.connect(self._show_confirm_dialog)
        layout.addWidget(confirm_btn)

        layout.addStretch()
        parent.addWidget(group)

    def _show_message_box(self):
        msg = MessageBox("Welcome", "This is a Fluent-styled message box dialog.\nIt supports multi-line content.", self.window())
        msg.exec()

    def _show_confirm_dialog(self):
        msg = MessageBox("Confirm Action", "Are you sure you want to proceed with this action?\nThis operation cannot be undone.", self.window())
        msg.yesButton.setText("Confirm")
        msg.cancelButton.setText("Cancel")
        msg.exec()

    def _build_progress_demo(self, parent):
        group = QGroupBox("Progress Feedback")
        self._track_group(group)
        layout = QVBoxLayout(group)

        btn_row = QHBoxLayout()
        self._download_btn = PushButton("Simulate Download")
        self._download_btn.setIcon(FIF.DOWNLOAD)
        self._download_btn.setFixedWidth(200)
        self._download_btn.clicked.connect(self._on_download_click)
        btn_row.addWidget(self._download_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._progress_bar = ProgressBar()
        self._progress_bar.setValue(0)
        layout.addWidget(self._progress_bar)

        self._progress_label = BodyLabel("Click the button to simulate a download with progress feedback.")
        layout.addWidget(self._progress_label)

        parent.addWidget(group)

    def _on_download_click(self):
        if self._progress_timer is not None:
            self._progress_timer.stop()
            self._progress_timer.timeout.disconnect()
        self._progress_bar.setValue(0)
        self._progress_val = 0
        self._download_btn.setEnabled(False)
        self._download_btn.setText("Downloading...")
        self._progress_label.setText("Downloading... 0%")
        self._progress_timer = QTimer(self)
        self._progress_timer.timeout.connect(self._tick_progress)
        self._progress_timer.start(50)

    def _tick_progress(self):
        self._progress_val += 2
        self._progress_bar.setValue(self._progress_val)
        self._progress_label.setText(f"Downloading... {self._progress_val}%")
        if self._progress_val >= 100:
            self._progress_timer.stop()
            self._download_btn.setEnabled(True)
            self._download_btn.setText("Simulate Download")
            self._progress_label.setText("Download completed!")

    def _build_state_tooltip(self, parent):
        group = QGroupBox("State ToolTip")
        self._track_group(group)
        layout = QVBoxLayout(group)

        btn_row = QHBoxLayout()
        tooltip_btn = PushButton("Show State ToolTip")
        tooltip_btn.clicked.connect(self._show_state_tooltip)
        btn_row.addWidget(tooltip_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addWidget(BodyLabel("A floating tooltip that shows operation state (loading/success/error)."))

        parent.addWidget(group)

    def _show_state_tooltip(self):
        if self._state_tooltip is not None:
            self._state_tooltip.close()
            self._state_tooltip = None
        self._state_tooltip = StateToolTip("Uploading...", "Please wait while the file is being uploaded", self.window())
        self._state_tooltip.move(self.window().width() - self._state_tooltip.width() - 30, 80)
        self._state_tooltip.show()

        self._tooltip_update_timer.start()
        self._tooltip_close_timer.start()

    def _on_tooltip_update(self):
        if self._state_tooltip is not None:
            self._state_tooltip.setContent("Upload completed!")

    def _on_tooltip_close(self):
        if self._state_tooltip is not None:
            self._state_tooltip.close()
            self._state_tooltip = None
