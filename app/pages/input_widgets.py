from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGridLayout, QGroupBox, QFormLayout)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             LineEdit, PasswordLineEdit, SearchLineEdit,
                             SpinBox, DoubleSpinBox, DateEdit, TimeEdit,
                             ComboBox, EditableComboBox, Slider, TextEdit,
                             FluentIcon as FIF, SwitchButton, StrongBodyLabel)

from app.theme_aware_page import ThemeAwarePage


class InputWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("inputWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Input Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Interactive input components for user data entry and selection.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_text_inputs(main_layout)
        self._build_numeric_inputs(main_layout)
        self._build_selectors(main_layout)
        self._build_slider_section(main_layout)
        self._build_text_edit(main_layout)

        main_layout.addStretch()

    def _build_text_inputs(self, parent):
        group = QGroupBox("Text Inputs")
        self._track_group(group)
        form = QFormLayout(group)
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        line_edit = LineEdit()
        line_edit.setPlaceholderText("Enter your name...")
        form.addRow("Line Edit:", line_edit)

        password_edit = PasswordLineEdit()
        password_edit.setPlaceholderText("Enter password...")
        form.addRow("Password:", password_edit)

        search_edit = SearchLineEdit()
        search_edit.setPlaceholderText("Search components...")
        form.addRow("Search:", search_edit)

        parent.addWidget(group)

    def _build_numeric_inputs(self, parent):
        group = QGroupBox("Numeric & Date Inputs")
        self._track_group(group)
        form = QFormLayout(group)
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        spin = SpinBox()
        spin.setRange(0, 100)
        spin.setValue(42)
        form.addRow("Spin Box:", spin)

        double_spin = DoubleSpinBox()
        double_spin.setRange(0.0, 1000.0)
        double_spin.setValue(3.14)
        form.addRow("Double Spin:", double_spin)

        date_edit = DateEdit()
        form.addRow("Date:", date_edit)

        time_edit = TimeEdit()
        form.addRow("Time:", time_edit)

        parent.addWidget(group)

    def _build_selectors(self, parent):
        group = QGroupBox("Selectors")
        self._track_group(group)
        form = QFormLayout(group)
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        combo = ComboBox()
        combo.addItems(["Fluent Design", "Material Design", "Apple HIG", "Ant Design"])
        combo.setCurrentIndex(0)
        form.addRow("Combo Box:", combo)

        editable_combo = EditableComboBox()
        editable_combo.addItems(["Python", "TypeScript", "Rust", "Go", "C++"])
        form.addRow("Editable Combo:", editable_combo)

        parent.addWidget(group)

    def _build_slider_section(self, parent):
        group = QGroupBox("Slider")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(16)

        slider = Slider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(60)
        layout.addWidget(slider)

        parent.addWidget(group)

    def _build_text_edit(self, parent):
        group = QGroupBox("Text Area")
        self._track_group(group)
        layout = QVBoxLayout(group)

        text_edit = TextEdit()
        text_edit.setPlaceholderText("Type your message here...")
        text_edit.setFixedHeight(120)
        layout.addWidget(text_edit)

        parent.addWidget(group)
