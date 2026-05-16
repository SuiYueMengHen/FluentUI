from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, BodyLabel, PushButton, FluentIcon as FIF, isDarkTheme)
from app.theme_aware_page import ThemeAwarePage
from app.components.command_palette import CommandPalette
from app.components.context_menu import ContextMenu
from app.components.drag_sortable_list import DragSortableList
from app.components.virtual_scroll_list import VirtualScrollList
from app.components.infinite_loader import InfiniteLoader
from app.components.pull_refresh import PullRefresh
from app.components.sticky_header import StickyHeader
from app.components.parallax_scroll import ParallaxScroll
from app.components.glass_card import GlassCard
from app.components.neon_border import NeonBorder
from app.components.gradient_text import GradientText
from app.components.particle_background import ParticleBackground
from app.components.morphing_shape import MorphingShape
from app.components.spotlight_card import SpotlightCard
from app.components.wave_divider import WaveDivider
from app.components.animated_border import AnimatedBorder


class AdvancedPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("advancedPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Advanced", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Advanced interaction components and decorative visual effects.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_command_palette(main_layout)
        self._build_context_menu(main_layout)
        self._build_drag_sortable_list(main_layout)
        self._build_virtual_scroll_list(main_layout)
        self._build_infinite_loader(main_layout)
        self._build_pull_refresh(main_layout)
        self._build_sticky_header(main_layout)
        self._build_parallax_scroll(main_layout)
        self._build_glass_card(main_layout)
        self._build_neon_border(main_layout)
        self._build_gradient_text(main_layout)
        self._build_particle_background(main_layout)
        self._build_morphing_shape(main_layout)
        self._build_spotlight_card(main_layout)
        self._build_wave_divider(main_layout)
        self._build_animated_border(main_layout)

        main_layout.addStretch()

    def _build_command_palette(self, parent):
        group = QGroupBox("Command Palette")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Searchable command palette with keyboard navigation and filtered results.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        palette = CommandPalette(commands=[
            "Open File", "Save", "Undo", "Redo",
            "Find", "Replace", "Toggle Theme", "Settings",
        ])
        layout.addWidget(palette, alignment=Qt.AlignmentFlag.AlignLeft)

        parent.addWidget(group)

    def _build_context_menu(self, parent):
        group = QGroupBox("Context Menu")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Popup context menu with scale animation and hover highlight for right-click actions.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        menu = ContextMenu(items=["Cut", "Copy", "Paste", "Delete", "Select All"])
        layout.addWidget(menu, alignment=Qt.AlignmentFlag.AlignLeft)

        parent.addWidget(group)

    def _build_drag_sortable_list(self, parent):
        group = QGroupBox("Drag Sortable List")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Reorderable list with drag-and-drop and slide animation for item rearrangement.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        drag_list = DragSortableList(items=["Item Alpha", "Item Beta", "Item Gamma", "Item Delta"])
        layout.addWidget(drag_list)

        parent.addWidget(group)

    def _build_virtual_scroll_list(self, parent):
        group = QGroupBox("Virtual Scroll List")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("High-performance virtualized list that only renders visible items for large datasets.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        items = [f"Row {i + 1}" for i in range(100)]
        vlist = VirtualScrollList(items=items)
        vlist.setFixedHeight(160)
        layout.addWidget(vlist)

        parent.addWidget(group)

    def _build_infinite_loader(self, parent):
        group = QGroupBox("Infinite Loader")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Infinite scroll loader with shimmer skeleton placeholders and load-more signal.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        loader = InfiniteLoader()
        loader.setFixedHeight(160)
        layout.addWidget(loader)

        parent.addWidget(group)

    def _build_pull_refresh(self, parent):
        group = QGroupBox("Pull Refresh")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Pull-to-refresh header with spinner animation and refresh request signal.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        refresh = PullRefresh()
        layout.addWidget(refresh)

        parent.addWidget(group)

    def _build_sticky_header(self, parent):
        group = QGroupBox("Sticky Header")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Sticky header bar with shadow transition on scroll for section anchoring.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        header = StickyHeader(title="Section Title")
        layout.addWidget(header)

        parent.addWidget(group)

    def _build_parallax_scroll(self, parent):
        group = QGroupBox("Parallax Scroll")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Multi-layer parallax scrolling effect with different scroll speeds per layer.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        parallax = ParallaxScroll()
        parallax.setFixedHeight(200)
        layout.addWidget(parallax)

        parent.addWidget(group)

    def _build_glass_card(self, parent):
        group = QGroupBox("Glass Card")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Frosted glass card with blur effect and semi-transparent background.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        card1 = GlassCard(title="Glass Card A")
        card2 = GlassCard(title="Glass Card B")

        row.addWidget(card1)
        row.addWidget(card2)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_neon_border(self, parent):
        group = QGroupBox("Neon Border")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Neon-glowing border with pulsing intensity animation for eye-catching highlights.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        neon1 = NeonBorder(color="#0078D4")
        neon2 = NeonBorder(color="#FF6B6B")

        row.addWidget(neon1)
        row.addWidget(neon2)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_gradient_text(self, parent):
        group = QGroupBox("Gradient Text")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Text rendered with animated gradient fill that shifts colors over time.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        text1 = GradientText(text="FluentUI Gallery", color1="#0078D4", color2="#6CCB5F")
        text2 = GradientText(text="Advanced Components", color1="#FF6B6B", color2="#FFB900")

        layout.addWidget(text1)
        layout.addWidget(text2)
        parent.addWidget(group)

    def _build_particle_background(self, parent):
        group = QGroupBox("Particle Background")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated floating particle system for decorative backgrounds with configurable density.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        particles = ParticleBackground(particle_count=40, color="#0078D4")
        particles.setFixedHeight(200)
        layout.addWidget(particles)

        parent.addWidget(group)

    def _build_morphing_shape(self, parent):
        group = QGroupBox("Morphing Shape")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Shape that smoothly morphs between circle, square, and star with interpolation animation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        shape1 = MorphingShape(color="#0078D4")
        shape2 = MorphingShape(color="#6CCB5F")
        shape3 = MorphingShape(color="#FF6B6B")

        row.addWidget(shape1)
        row.addWidget(shape2)
        row.addWidget(shape3)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_spotlight_card(self, parent):
        group = QGroupBox("Spotlight Card")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Card with mouse-following spotlight effect that illuminates content on hover.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        card1 = SpotlightCard(title="Hover Me")
        card2 = SpotlightCard(title="And Me")

        row.addWidget(card1)
        row.addWidget(card2)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_wave_divider(self, parent):
        group = QGroupBox("Wave Divider")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated wave divider with flowing sine motion for section separation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        wave = WaveDivider(color="#0078D4")
        layout.addWidget(wave)

        parent.addWidget(group)

    def _build_animated_border(self, parent):
        group = QGroupBox("Animated Border")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Card with rotating conic-gradient border animation for dynamic framing effects.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        border1 = AnimatedBorder(title="Rotating Border")
        border2 = AnimatedBorder(title="Glow Frame")

        row.addWidget(border1)
        row.addWidget(border2)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)
