from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QStackedWidget)
from PySide6.QtCore import Qt
from qfluentwidgets import (TitleLabel, SubtitleLabel, BodyLabel,
                             Pivot, SegmentedWidget, TabBar, BreadcrumbBar,
                             FluentIcon as FIF, PushButton)

from app.theme_aware_page import ThemeAwarePage


class NavigationWidgetsPage(ThemeAwarePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("navigationWidgetsPage")

        container = QWidget()
        self.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(40, 32, 40, 32)
        main_layout.setSpacing(24)

        title = TitleLabel("Navigation Widgets", self)
        self._track_title(title)
        main_layout.addWidget(title)

        desc = BodyLabel("Components for navigating between pages, sections, and content areas.")
        self._track_label(desc, "secondary")
        main_layout.addWidget(desc)
        main_layout.addSpacing(8)

        self._build_breadcrumb(main_layout)
        self._build_pivot(main_layout)
        self._build_segmented(main_layout)
        self._build_tabbar(main_layout)

        main_layout.addStretch()

    def _build_breadcrumb(self, parent):
        group = QGroupBox("Breadcrumb Bar")
        self._track_group(group)
        layout = QVBoxLayout(group)

        breadcrumb = BreadcrumbBar()
        breadcrumb.addItem("home", "Home")
        breadcrumb.addItem("components", "Components")
        breadcrumb.addItem("navigation", "Navigation")
        breadcrumb.setCurrentIndex(2)
        layout.addWidget(breadcrumb)

        parent.addWidget(group)

    def _build_pivot(self, parent):
        group = QGroupBox("Pivot (Tab Switcher)")
        self._track_group(group)
        layout = QVBoxLayout(group)

        pivot = Pivot()
        stack = QStackedWidget()

        pages = [
            ("overview", "Overview", "This is the overview page with general information."),
            ("details", "Details", "Detailed content and specifications are shown here."),
            ("settings", "Settings", "Configure preferences and application settings."),
        ]

        for key, name, content in pages:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.addWidget(BodyLabel(content))
            stack.addWidget(page)
            pivot.addItem(
                routeKey=key,
                text=name,
                onClick=lambda checked, k=key: stack.setCurrentIndex([p[0] for p in pages].index(k))
            )

        pivot.setCurrentItem("overview")
        stack.setCurrentIndex(0)

        layout.addWidget(pivot)
        layout.addWidget(stack)

        parent.addWidget(group)

    def _build_segmented(self, parent):
        group = QGroupBox("Segmented Widget")
        self._track_group(group)
        layout = QVBoxLayout(group)

        segmented = SegmentedWidget()
        seg_stack = QStackedWidget()

        items = [
            ("day", "Day", "Day mode is active with bright colors."),
            ("week", "Week", "Weekly view showing 7-day schedule."),
            ("month", "Month", "Monthly calendar overview."),
        ]

        for key, text, content in items:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.addWidget(BodyLabel(content))
            seg_stack.addWidget(page)
            segmented.addItem(
                routeKey=key,
                text=text,
                onClick=lambda checked, k=key: seg_stack.setCurrentIndex([i[0] for i in items].index(k))
            )

        segmented.setCurrentItem("day")
        seg_stack.setCurrentIndex(0)

        layout.addWidget(segmented)
        layout.addWidget(seg_stack)

        parent.addWidget(group)

    def _build_tabbar(self, parent):
        group = QGroupBox("Tab Bar")
        self._track_group(group)
        layout = QVBoxLayout(group)

        tab_bar = TabBar()
        tab_bar.setTabMaximumWidth(160)
        tab_bar.addTab("document", "Document", icon=FIF.DOCUMENT)
        tab_bar.addTab("gallery", "Gallery", icon=FIF.PHOTO)
        tab_bar.addTab("music", "Music", icon=FIF.MUSIC)
        tab_bar.addTab("video", "Video", icon=FIF.VIDEO)
        tab_bar.setCurrentIndex(0)

        layout.addWidget(tab_bar)

        parent.addWidget(group)
