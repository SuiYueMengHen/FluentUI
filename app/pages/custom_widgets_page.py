from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             CardWidget, StrongBodyLabel, PushButton,
                             FluentIcon as FIF, isDarkTheme, setTheme, Theme)

from app.theme_aware_page import ThemeAwarePage
from app.components.gradient_card import GradientCard
from app.components.status_indicator import StatusIndicator
from app.components.avatar_ring import AvatarRing
from app.components.progress_ring import ProgressRing
from app.components.glow_button import GlowButton
from app.components.typing_text import TypingText
from app.components.color_palette_card import ColorPaletteCard
from app.components.stat_card import StatCard
from app.components.shimmer_widget import ShimmerWidget
from app.components.animated_toggle import AnimatedToggle
from app.components.notification_badge import NotificationBadge
from app.components.wave_progress import WaveProgress
from app.components.flip_card import FlipCard
from app.components.animated_counter import AnimatedCounter
from app.components.accordion_card import AccordionCard
from app.components.segmented_widget import SegmentedWidget
from app.components.toast import Toast
from app.components.expand_group import ExpandGroup
from app.components.ripple_button import RippleButton


class CustomWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("customWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Custom Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Handcrafted components built with QPainter, QPropertyAnimation, and Fluent Design principles.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_gradient_cards(main_layout)
        self._build_status_indicators(main_layout)
        self._build_avatar_rings(main_layout)
        self._build_progress_rings(main_layout)
        self._build_glow_buttons(main_layout)
        self._build_typing_text(main_layout)
        self._build_shimmer(main_layout)
        self._build_animated_toggles(main_layout)
        self._build_notification_badges(main_layout)
        self._build_wave_progress(main_layout)
        self._build_flip_cards(main_layout)
        self._build_animated_counters(main_layout)
        self._build_accordion_cards(main_layout)
        self._build_segmented_widgets(main_layout)
        self._build_toasts(main_layout)
        self._build_expand_groups(main_layout)
        self._build_ripple_buttons(main_layout)

        main_layout.addStretch()

    def _build_gradient_cards(self, parent):
        group = QGroupBox("Gradient Card")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Cards with gradient backgrounds, hover animation, and customizable colors.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        card1 = GradientCard("Ocean Blue", "Horizontal gradient with hover effect", color1="#0078D4", color2="#005A9E")
        card2 = GradientCard("Sunset Glow", "Warm gradient with vertical direction", color1="#FF6B6B", color2="#FFB900", direction="vertical")
        card3 = GradientCard("Forest Green", "Nature-inspired gradient palette", color1="#0F7B0F", color2="#6CCB5F")

        cards_row.addWidget(card1)
        cards_row.addWidget(card2)
        cards_row.addWidget(card3)

        layout.addLayout(cards_row)
        parent.addWidget(group)

    def _build_status_indicators(self, parent):
        group = QGroupBox("Status Indicator")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated status dots with breathing light effect. Supports online, offline, busy, and away states.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        for status, label_text in [
            (StatusIndicator.ONLINE, "Online"),
            (StatusIndicator.OFFLINE, "Offline"),
            (StatusIndicator.BUSY, "Busy"),
            (StatusIndicator.AWAY, "Away"),
        ]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            indicator = StatusIndicator(status=status, size=14)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(indicator, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_avatar_rings(self, parent):
        group = QGroupBox("Avatar Ring")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Circular avatar with gradient ring border and optional online status indicator.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        configs = [
            (64, "#0078D4", "#60CDFF", True, "#6CCB5F", "Default"),
            (48, "#FF6B6B", "#FFB900", True, "#FF6B6B", "Busy"),
            (56, "#6CCB5F", "#0F7B0F", False, None, "No Status"),
            (40, "#9E9E9E", "#616161", True, "#9E9E9E", "Offline"),
        ]

        for size, c1, c2, show_status, status_color, label_text in configs:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            avatar = AvatarRing(size=size, ring_color1=c1, ring_color2=c2)
            if show_status:
                avatar.set_status(True, status_color)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_progress_rings(self, parent):
        group = QGroupBox("Progress Ring")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Circular progress indicator with gradient stroke. Supports determinate and indeterminate modes.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        ring1 = ProgressRing(size=80, stroke_width=6)
        ring1.set_value(75)

        ring2 = ProgressRing(size=80, stroke_width=6, color1="#6CCB5F", color2="#0F7B0F")
        ring2.set_value(42)

        ring3 = ProgressRing(size=80, stroke_width=6, color1="#FF6B6B", color2="#FFB900")
        ring3.set_indeterminate(True)

        for ring, label_text in [(ring1, "75%"), (ring2, "42%"), (ring3, "Loading...")]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(ring, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_glow_buttons(self, parent):
        group = QGroupBox("Glow Button")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Enhanced push button with hover glow effect and press feedback.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        btn1 = GlowButton("Primary Action", accent_color="#0078D4")
        btn2 = GlowButton("Success", accent_color="#0F7B0F")
        btn3 = GlowButton("Danger", accent_color="#C42B1C")
        btn4 = GlowButton("Warning", accent_color="#9D5D00")

        row.addWidget(btn1)
        row.addWidget(btn2)
        row.addWidget(btn3)
        row.addWidget(btn4)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_typing_text(self, parent):
        group = QGroupBox("Typing Text")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated text that types character by character with a blinking cursor.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        typing1 = TypingText("Hello, FluentUI Gallery! Welcome to the custom components showcase.", typing_speed=60)
        self._track_label(typing1)

        typing2 = TypingText("This component supports configurable typing speed and loop mode.", typing_speed=80, loop=True)
        self._track_label(typing2, "secondary")

        layout.addWidget(typing1)
        layout.addWidget(typing2)

        btn_row = QHBoxLayout()
        start_btn = PushButton("Start Typing")
        start_btn.clicked.connect(lambda: (typing1.start_typing(), typing2.start_typing()))
        stop_btn = PushButton("Show All")
        stop_btn.clicked.connect(lambda: (typing1.stop_typing(), typing2.stop_typing()))
        btn_row.addWidget(start_btn)
        btn_row.addWidget(stop_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._typing1_delay_timer = QTimer(self)
        self._typing1_delay_timer.setSingleShot(True)
        self._typing1_delay_timer.setInterval(800)
        self._typing1_delay_timer.timeout.connect(typing1.start_typing)
        self._typing1_delay_timer.start()

        self._typing2_delay_timer = QTimer(self)
        self._typing2_delay_timer.setSingleShot(True)
        self._typing2_delay_timer.setInterval(3500)
        self._typing2_delay_timer.timeout.connect(typing2.start_typing)
        self._typing2_delay_timer.start()

        parent.addWidget(group)

    def _build_shimmer(self, parent):
        group = QGroupBox("Shimmer / Skeleton")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Loading placeholder with shimmer animation. Used as skeleton screen during data loading.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        shimmer_row = QHBoxLayout()
        shimmer_row.setSpacing(16)

        circle = ShimmerWidget(48, 48, shape=ShimmerWidget.CIRCLE)
        shimmer_row.addWidget(circle)

        lines = QVBoxLayout()
        lines.setSpacing(8)
        lines.addWidget(ShimmerWidget(200, 16))
        lines.addWidget(ShimmerWidget(160, 12))
        lines.addWidget(ShimmerWidget(120, 12))
        shimmer_row.addLayout(lines)

        shimmer_row.addStretch()
        layout.addLayout(shimmer_row)

        parent.addWidget(group)

    def _build_animated_toggles(self, parent):
        group = QGroupBox("Animated Toggle")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Toggle switch with spring animation. Supports custom on/off colors and smooth transitions.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        toggle1 = AnimatedToggle(on_color="#0078D4")
        toggle1.set_checked(True)
        toggle2 = AnimatedToggle(on_color="#6CCB5F")
        toggle3 = AnimatedToggle(on_color="#FF6B6B")

        for toggle, label_text in [(toggle1, "Primary"), (toggle2, "Success"), (toggle3, "Danger")]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(toggle, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_notification_badges(self, parent):
        group = QGroupBox("Notification Badge")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Pulsing badge with count display. Animates on count change with scale effect.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        badges_data = [
            (3, "#FF4444", "Messages"),
            (12, "#0078D4", "Updates"),
            (99, "#6CCB5F", "Tasks"),
        ]

        self._badges = []
        for count, color, label_text in badges_data:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge = NotificationBadge(count=count, color=color)
            self._badges.append(badge)
            label = QLabel(label_text)
            self._track_label(label, "secondary")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(badge, alignment=Qt.AlignmentFlag.AlignCenter)
            col.addWidget(label)
            row.addLayout(col)

        btn_row = QHBoxLayout()
        increment_btn = PushButton("Increment")
        increment_btn.clicked.connect(self._increment_badges)
        btn_row.addWidget(increment_btn)
        btn_row.addStretch()
        layout.addLayout(row)
        layout.addLayout(btn_row)

        parent.addWidget(group)

    def _increment_badges(self):
        for badge in getattr(self, '_badges', []):
            current = badge._count
            badge.set_count(current + 1)

    def _build_wave_progress(self, parent):
        group = QGroupBox("Wave Progress")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Fluid wave animation progress bar with dual-layer sine waves and smooth value transitions.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(24)

        self._wave1 = WaveProgress()
        self._wave1.set_value(65)

        self._wave2 = WaveProgress()
        self._wave2.set_value(30)

        row.addWidget(self._wave1)
        row.addWidget(self._wave2)
        row.addStretch()

        layout.addLayout(row)

        btn_row = QHBoxLayout()
        randomize_btn = PushButton("Randomize")
        randomize_btn.clicked.connect(self._randomize_waves)
        btn_row.addWidget(randomize_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        parent.addWidget(group)

    def _randomize_waves(self):
        import random
        self._wave1.set_value(random.randint(10, 90))
        self._wave2.set_value(random.randint(10, 90))

    def _build_flip_cards(self, parent):
        group = QGroupBox("Flip Card")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("3D flip card with click-to-reveal animation. Set custom front and back content.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        for title_text, back_text, color in [
            ("Click to Flip", "Back Side!", "#0078D4"),
            ("Details", "Hidden Info", "#6CCB5F"),
        ]:
            card = FlipCard()
            front = QWidget()
            front_layout = QVBoxLayout(front)
            front_layout.setContentsMargins(20, 16, 20, 16)
            front_label = QLabel(title_text)
            front_label.setStyleSheet("font-size: 16px; font-weight: 600; background: transparent;")
            front_layout.addWidget(front_label)
            front_layout.addStretch()

            back = QWidget()
            back_layout = QVBoxLayout(back)
            back_layout.setContentsMargins(20, 16, 20, 16)
            back_label = QLabel(back_text)
            back_label.setStyleSheet(f"font-size: 14px; color: {color}; background: transparent;")
            back_layout.addWidget(back_label)
            back_layout.addStretch()

            card.set_front(front)
            card.set_back(back)
            row.addWidget(card)

        row.addStretch()
        layout.addLayout(row)
        parent.addWidget(group)

    def _build_animated_counters(self, parent):
        group = QGroupBox("Animated Counter")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Number rolling animation with smooth transitions. Supports prefix and suffix.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(32)

        self._counter1 = AnimatedCounter(font_size=36)
        self._counter1.set_value(42)

        self._counter2 = AnimatedCounter(font_size=36, prefix="$")
        self._counter2.set_value(1280)

        self._counter3 = AnimatedCounter(font_size=36, suffix="%")
        self._counter3.set_value(75)

        row.addWidget(self._counter1)
        row.addWidget(self._counter2)
        row.addWidget(self._counter3)
        row.addStretch()

        layout.addLayout(row)

        btn_row = QHBoxLayout()
        randomize_btn = PushButton("Randomize")
        randomize_btn.clicked.connect(self._randomize_counters)
        btn_row.addWidget(randomize_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        parent.addWidget(group)

    def _randomize_counters(self):
        import random
        self._counter1.set_value(random.randint(0, 999))
        self._counter2.set_value(random.randint(100, 9999))
        self._counter3.set_value(random.randint(0, 100))

    def _build_accordion_cards(self, parent):
        group = QGroupBox("Accordion Card")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Expandable card with smooth height animation and rotating arrow indicator.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        acc1 = AccordionCard("Getting Started")
        content1 = QWidget()
        content1_layout = QVBoxLayout(content1)
        content1_layout.setContentsMargins(16, 8, 16, 8)
        content1_layout.addWidget(BodyLabel("Welcome to FluentUI Gallery! This showcase demonstrates modern desktop components."))
        acc1.set_content(content1)
        acc1.set_expanded(True, animate=False)

        acc2 = AccordionCard("Advanced Features")
        content2 = QWidget()
        content2_layout = QVBoxLayout(content2)
        content2_layout.setContentsMargins(16, 8, 16, 8)
        content2_layout.addWidget(BodyLabel("Explore custom animations, theme support, and rich interactive components."))
        acc2.set_content(content2)

        layout.addWidget(acc1)
        layout.addWidget(acc2)
        parent.addWidget(group)

    def _build_segmented_widgets(self, parent):
        group = QGroupBox("Segmented Widget")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Animated tab selector with sliding indicator. Supports custom segments and selection callback.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        seg1 = SegmentedWidget(["Day", "Week", "Month", "Year"])
        seg1.set_current_index(1)

        seg2 = SegmentedWidget(["List", "Grid", "Board"])
        seg2.set_current_index(0)

        layout.addWidget(seg1)
        layout.addSpacing(8)
        layout.addWidget(seg2)
        parent.addWidget(group)

    def _build_toasts(self, parent):
        group = QGroupBox("Toast Notification")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Auto-dismissing notification with slide-in/fade-out animation. Supports info, success, warning, and error types.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(12)

        info_btn = PushButton("Info")
        info_btn.setIcon(FIF.INFO)
        info_btn.clicked.connect(lambda: Toast.show("This is an informational message.", "info", self))

        success_btn = PushButton("Success")
        success_btn.setIcon(FIF.COMPLETED)
        success_btn.clicked.connect(lambda: Toast.show("Operation completed successfully!", "success", self))

        warning_btn = PushButton("Warning")
        warning_btn.setIcon(FIF.RINGER)
        warning_btn.clicked.connect(lambda: Toast.show("Please review before proceeding.", "warning", self))

        error_btn = PushButton("Error")
        error_btn.setIcon(FIF.CLOSE)
        error_btn.clicked.connect(lambda: Toast.show("Something went wrong. Please try again.", "error", self))

        row.addWidget(info_btn)
        row.addWidget(success_btn)
        row.addWidget(warning_btn)
        row.addWidget(error_btn)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)

    def _build_expand_groups(self, parent):
        group = QGroupBox("Expand Group")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Collapsible group with animated expand/collapse and arrow rotation.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        eg1 = ExpandGroup("Project Files")
        eg_content1 = QWidget()
        eg_layout1 = QVBoxLayout(eg_content1)
        eg_layout1.setContentsMargins(16, 8, 16, 8)
        eg_layout1.addWidget(BodyLabel("main.py"))
        eg_layout1.addWidget(BodyLabel("app/__init__.py"))
        eg_layout1.addWidget(BodyLabel("app/main_window.py"))
        eg1.set_content(eg_content1)
        eg1.set_expanded(True, animate=False)

        eg2 = ExpandGroup("Dependencies")
        eg_content2 = QWidget()
        eg_layout2 = QVBoxLayout(eg_content2)
        eg_layout2.setContentsMargins(16, 8, 16, 8)
        eg_layout2.addWidget(BodyLabel("PySide6 >= 6.5"))
        eg_layout2.addWidget(BodyLabel("qfluentwidgets >= 1.4"))
        eg2.set_content(eg_content2)

        layout.addWidget(eg1)
        layout.addWidget(eg2)
        parent.addWidget(group)

    def _build_ripple_buttons(self, parent):
        group = QGroupBox("Ripple Button")
        self._track_group(group)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        desc = BodyLabel("Button with Material-style ripple effect expanding from click position and press scale feedback.")
        self._track_label(desc, "secondary")
        layout.addWidget(desc)

        row = QHBoxLayout()
        row.setSpacing(16)

        btn1 = RippleButton("Primary", accent_color="#0078D4")
        btn2 = RippleButton("Success", accent_color="#0F7B0F")
        btn3 = RippleButton("Danger", accent_color="#C42B1C")
        btn4 = RippleButton("Warning", accent_color="#9D5D00")

        row.addWidget(btn1)
        row.addWidget(btn2)
        row.addWidget(btn3)
        row.addWidget(btn4)
        row.addStretch()

        layout.addLayout(row)
        parent.addWidget(group)
