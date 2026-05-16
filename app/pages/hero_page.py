from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGridLayout, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt, QTimer
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             PrimaryPushButton, PushButton, FluentIcon as FIF,
                             CardWidget, IconWidget, isDarkTheme, setTheme, Theme)

from app.theme_aware_page import ThemeAwarePage
from app.components.gradient_card import GradientCard
from app.components.typing_text import TypingText
from app.components.stat_card import StatCard
from app.components.color_palette_card import ColorPaletteCard


class FeatureCard(CardWidget):
    def __init__(self, icon, title, description, parent=None):
        super().__init__(parent)
        self.setFixedHeight(140)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        icon_label = IconWidget(icon, self)
        icon_label.setFixedSize(32, 32)

        title_label = QLabel(title, self)
        self._title_label = title_label
        self._update_title_style()

        self._desc_label = QLabel(description, self)
        self._update_desc_style()
        self._desc_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addSpacing(8)
        layout.addWidget(title_label)
        layout.addSpacing(4)
        layout.addWidget(self._desc_label)
        layout.addStretch()

    def _update_title_style(self):
        color = "#1A1A1A" if not isDarkTheme() else "#FFFFFF"
        self._title_label.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {color}; background: transparent;")

    def _update_desc_style(self):
        color = "#9E9E9E" if isDarkTheme() else "#616161"
        self._desc_label.setStyleSheet(f"font-size: 13px; color: {color}; background: transparent;")

    def refresh_theme(self):
        self._update_title_style()
        self._update_desc_style()


class HeroPage(ThemeAwarePage):
    @staticmethod
    def _make_transparent(widget):
        widget.setAutoFillBackground(False)
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 0))
        widget.setPalette(palette)
        widget.setStyleSheet(widget.styleSheet() + " background: transparent; background-color: rgba(0,0,0,0);")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("heroPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(32)

        self._build_hero_banner(main_layout)
        self._build_feature_cards(main_layout)
        self._build_stats_section(main_layout)
        self._build_palette_section(main_layout)

        main_layout.addStretch()

    def _build_hero_banner(self, parent_layout):
        banner = GradientCard(
            color1="#0078D4",
            color2="#005A9E",
            direction="vertical",
            auto_layout=False
        )
        banner.setFixedHeight(220)

        banner_layout = banner.content_layout
        banner_layout.setContentsMargins(40, 32, 40, 32)
        banner_layout.setSpacing(8)

        title = TitleLabel("FluentUI Gallery", banner)
        title.setStyleSheet("color: white; font-size: 36px; font-weight: 700;")
        self._make_transparent(title)

        typing = TypingText("Modern Desktop Component Showcase with Fluent Design", typing_speed=50, parent=banner)
        typing.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 16px;")
        self._make_transparent(typing)

        self._banner_title = title
        self._banner_typing = typing

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        browse_btn = PrimaryPushButton("Browse Components", banner)
        browse_btn.setIcon(FIF.SEARCH)
        browse_btn.setFixedWidth(200)
        browse_btn.setFixedHeight(40)

        github_btn = PushButton("View Source", banner)
        github_btn.setIcon(FIF.GITHUB)
        github_btn.setFixedWidth(160)
        github_btn.setFixedHeight(40)

        btn_row.addWidget(browse_btn)
        btn_row.addWidget(github_btn)
        btn_row.addStretch()

        banner_layout.addWidget(title)
        banner_layout.addWidget(typing)
        banner_layout.addSpacing(12)
        banner_layout.addLayout(btn_row)
        banner_layout.addStretch()

        parent_layout.addWidget(banner)

        self._typing_delay_timer = QTimer(self)
        self._typing_delay_timer.setSingleShot(True)
        self._typing_delay_timer.setInterval(500)
        self._typing_delay_timer.timeout.connect(typing.start_typing)
        self._typing_delay_timer.start()

    def _build_feature_cards(self, parent_layout):
        section_title = SubtitleLabel("Features", self)
        self._track_section_title(section_title)
        parent_layout.addWidget(section_title)

        grid = QGridLayout()
        grid.setSpacing(16)

        features = [
            (FIF.PALETTE, "Fluent Design", "Built on Microsoft Fluent Design System with Mica, Acrylic, and smooth animations"),
            (FIF.CONSTRACT, "Dark & Light Mode", "Seamless theme switching with automatic system detection and manual override"),
            (FIF.CERTIFICATE, "300+ Icons", "Comprehensive FluentIcon library with consistent stroke width and visual language"),
            (FIF.APPLICATION, "Custom Components", "Handcrafted widgets including gradient cards, progress rings, glow buttons and more"),
        ]

        self._feature_cards = []
        for i, (icon, title, desc) in enumerate(features):
            card = FeatureCard(icon, title, desc, self)
            self._feature_cards.append(card)
            grid.addWidget(card, i // 2, i % 2)

        parent_layout.addLayout(grid)

    def _build_stats_section(self, parent_layout):
        section_title = SubtitleLabel("At a Glance", self)
        self._track_section_title(section_title)
        parent_layout.addWidget(section_title)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        stats = [
            ("50+", "Components", FIF.TILES, "+12", "#0078D4"),
            ("9", "Custom Widgets", FIF.PALETTE, "New", "#6CCB5F"),
            ("300+", "Fluent Icons", FIF.BRIGHTNESS, "+50", "#FFB900"),
            ("2", "Theme Modes", FIF.CONSTRACT, "Auto", "#60CDFF"),
        ]

        for value, title, icon, trend, color in stats:
            card = StatCard(title=title, value=value, icon=icon, trend=trend, accent_color=color, parent=self)
            stats_row.addWidget(card)

        parent_layout.addLayout(stats_row)

    def _build_palette_section(self, parent_layout):
        section_title = SubtitleLabel("Color Palette", self)
        self._track_section_title(section_title)
        parent_layout.addWidget(section_title)

        palette_card = ColorPaletteCard("Fluent Design Colors", parent=self)
        parent_layout.addWidget(palette_card)

    def refresh_theme(self):
        super().refresh_theme()
        for card in getattr(self, '_feature_cards', []):
            card.refresh_theme()
        for w in (getattr(self, '_banner_title', None), getattr(self, '_banner_typing', None)):
            if w:
                self._make_transparent(w)
