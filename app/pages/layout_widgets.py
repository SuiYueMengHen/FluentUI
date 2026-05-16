from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QFrame)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             ExpandLayout, FlowLayout, CardWidget,
                             HorizontalSeparator, PushButton, FluentIcon as FIF,
                             StrongBodyLabel, isDarkTheme)

from app.theme_aware_page import ThemeAwarePage


class LayoutWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("layoutWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Layout Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Layout components for organizing and structuring your interface.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_expand_layout(main_layout)
        self._build_flow_layout(main_layout)
        self._build_separator(main_layout)
        self._build_card_layouts(main_layout)

        main_layout.addStretch()

    def _build_expand_layout(self, parent):
        group = QGroupBox("Expand Layout (Accordion)")
        self._track_group(group)
        layout = QVBoxLayout(group)

        expand_layout = ExpandLayout()
        expand_layout.setSpacing(8)

        sections = [
            ("General Settings", "Configure application behavior and preferences"),
            ("Appearance", "Customize theme, colors, and visual elements"),
            ("Advanced", "Configure advanced options and developer settings"),
        ]

        for title_text, desc_text in sections:
            card = CardWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 12, 20, 12)
            card_layout.addWidget(StrongBodyLabel(title_text))
            card_layout.addWidget(BodyLabel(desc_text))
            card.setFixedHeight(80)
            expand_layout.addWidget(card)

        layout.addLayout(expand_layout)
        parent.addWidget(group)

    def _build_flow_layout(self, parent):
        group = QGroupBox("Flow Layout")
        self._track_group(group)
        layout = QVBoxLayout(group)

        flow_container = QWidget()
        flow_layout = FlowLayout(flow_container, needAni=True)
        flow_layout.setSpacing(8)

        tags = [
            "Fluent Design", "PySide6", "Dark Mode", "Mica Effect",
            "Acrylic", "Animation", "Navigation", "Component Gallery",
            "Custom Widgets", "SVG Icons", "Responsive", "Modern UI",
        ]

        for tag in tags:
            btn = PushButton(tag)
            btn.setFixedHeight(32)
            flow_layout.addWidget(btn)

        layout.addWidget(flow_container)
        parent.addWidget(group)

    def _build_separator(self, parent):
        group = QGroupBox("Separator")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        layout.addWidget(BodyLabel("Section A"))
        layout.addWidget(HorizontalSeparator())
        layout.addWidget(BodyLabel("Section B"))
        layout.addWidget(HorizontalSeparator())
        layout.addWidget(BodyLabel("Section C"))

        parent.addWidget(group)

    def _build_card_layouts(self, parent):
        group = QGroupBox("Card Layout Variations")
        self._track_group(group)
        layout = QHBoxLayout(group)
        layout.setSpacing(16)

        for i, (title_text, desc_text) in enumerate([
            ("Simple Card", "Basic card with content"),
            ("Icon Card", "Card with icon header"),
            ("Action Card", "Card with action buttons"),
        ]):
            card = CardWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 16, 20, 16)
            card_layout.setSpacing(8)

            card_layout.addWidget(StrongBodyLabel(title_text))
            card_layout.addWidget(BodyLabel(desc_text))

            if i == 2:
                btn = PushButton("Action")
                btn.setFixedWidth(100)
                card_layout.addWidget(btn)

            card_layout.addStretch()
            card.setFixedWidth(200)
            layout.addWidget(card)

        layout.addStretch()
        parent.addWidget(group)
