from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.floating_label_input import FloatingLabelInput
from app.components.otp_input import OTPInput
from app.components.credit_card_input import CreditCardInput
from app.components.stepper_input import StepperInput
from app.components.color_tag_input import ColorTagInput
from app.components.multi_select import MultiSelect
from app.components.date_range_picker import DateRangePicker
from app.components.file_drop_zone import FileDropZone


class FormEnhancedPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("formEnhancedPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Form Enhanced", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Advanced form components with rich interactions and animations.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_floating_label_input(main_layout)
        self._build_otp_input(main_layout)
        self._build_credit_card_input(main_layout)
        self._build_stepper_input(main_layout)
        self._build_color_tag_input(main_layout)
        self._build_multi_select(main_layout)
        self._build_date_range_picker(main_layout)
        self._build_file_drop_zone(main_layout)

        main_layout.addStretch()

    def _build_floating_label_input(self, parent):
        group = QGroupBox("Floating Label Input")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Text input with animated floating label that moves above on focus or when filled.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        name_input = FloatingLabelInput(label="Full Name", placeholder="Enter your name")
        email_input = FloatingLabelInput(label="Email", placeholder="Enter your email")

        row.addWidget(name_input)
        row.addWidget(email_input)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_otp_input(self, parent):
        group = QGroupBox("OTP Input")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("One-time password input with auto-focus progression and box scale animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        otp = OTPInput(length=6)
        layout.addWidget(otp)
        parent.addWidget(group)

    def _build_credit_card_input(self, parent):
        group = QGroupBox("Credit Card Input")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Credit card form with live card preview, flip animation for CVV, and number formatting.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        card = CreditCardInput()
        layout.addWidget(card)
        parent.addWidget(group)

    def _build_stepper_input(self, parent):
        group = QGroupBox("Stepper Input")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Numeric stepper with increment/decrement buttons and scroll wheel animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        stepper = StepperInput(value=5, min_val=0, max_val=99)
        layout.addWidget(stepper)
        parent.addWidget(group)

    def _build_color_tag_input(self, parent):
        group = QGroupBox("Color Tag Input")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Tag input with colored chips, inline creation, and removable items with pop animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        tags = ColorTagInput(tags=["Design", "Frontend", "PySide6"])
        layout.addWidget(tags)
        parent.addWidget(group)

    def _build_multi_select(self, parent):
        group = QGroupBox("Multi Select")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Dropdown multi-select with expand animation and checkbox-style item selection.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        select = MultiSelect(options=["Option A", "Option B", "Option C", "Option D"])
        layout.addWidget(select)
        parent.addWidget(group)

    def _build_date_range_picker(self, parent):
        group = QGroupBox("Date Range Picker")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Calendar-based date range picker with month navigation and range highlighting.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        picker = DateRangePicker()
        layout.addWidget(picker)
        parent.addWidget(group)

    def _build_file_drop_zone(self, parent):
        group = QGroupBox("File Drop Zone")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Drag-and-drop file zone with pulse animation on hover and visual drag-over feedback.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        zone = FileDropZone(label="Drop files here or click to browse")
        layout.addWidget(zone, alignment=Qt.AlignmentFlag.AlignLeft)

        parent.addWidget(group)
