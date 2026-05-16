from PySide6.QtCore import Qt
from qfluentwidgets import (FluentWindow, NavigationItemPosition, FluentIcon as FIF,
                             setTheme, Theme, isDarkTheme)

from app.pages.hero_page import HeroPage
from app.pages.basic_widgets import BasicWidgetsPage
from app.pages.input_widgets import InputWidgetsPage
from app.pages.navigation_widgets import NavigationWidgetsPage
from app.pages.feedback_widgets import FeedbackWidgetsPage
from app.pages.data_widgets import DataWidgetsPage
from app.pages.layout_widgets import LayoutWidgetsPage
from app.pages.custom_widgets_page import CustomWidgetsPage
from app.pages.charts_page import ChartsPage
from app.pages.diagrams_page import DiagramsPage
from app.pages.social_page import SocialPage
from app.pages.media_page import MediaPage
from app.pages.form_enhanced_page import FormEnhancedPage
from app.pages.status_page import StatusPage
from app.pages.advanced_page import AdvancedPage
from app.theme_manager import ThemeManager


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self._theme_manager = ThemeManager()

        self.setWindowTitle("FluentUI Gallery")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 800)

        self._init_pages()
        self._init_navigation()
        self._init_theme_action()

        self._theme_manager.set_theme(self._theme_manager.current_theme)

    def _init_pages(self):
        self.hero_page = HeroPage(self)
        self.basic_widgets_page = BasicWidgetsPage(self)
        self.input_widgets_page = InputWidgetsPage(self)
        self.navigation_widgets_page = NavigationWidgetsPage(self)
        self.feedback_widgets_page = FeedbackWidgetsPage(self)
        self.data_widgets_page = DataWidgetsPage(self)
        self.layout_widgets_page = LayoutWidgetsPage(self)
        self.custom_widgets_page = CustomWidgetsPage(self)
        self.charts_page = ChartsPage(self)
        self.diagrams_page = DiagramsPage(self)
        self.social_page = SocialPage(self)
        self.media_page = MediaPage(self)
        self.form_enhanced_page = FormEnhancedPage(self)
        self.status_page = StatusPage(self)
        self.advanced_page = AdvancedPage(self)

    def _init_navigation(self):
        self.addSubInterface(
            self.hero_page, FIF.HOME, "Home",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.basic_widgets_page, FIF.CHECKBOX, "Basic",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.input_widgets_page, FIF.EDIT, "Input",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.navigation_widgets_page, FIF.MENU, "Navigation",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.feedback_widgets_page, FIF.INFO, "Feedback",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.data_widgets_page, FIF.TILES, "Data",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.layout_widgets_page, FIF.LAYOUT, "Layout",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.custom_widgets_page, FIF.PALETTE, "Custom",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.charts_page, FIF.PIE_SINGLE, "Charts",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.diagrams_page, FIF.DICTIONARY, "Diagrams",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.social_page, FIF.HEART, "Social",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.media_page, FIF.MEDIA, "Media",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.form_enhanced_page, FIF.EDIT, "Form+",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.status_page, FIF.SYNC, "Status",
            NavigationItemPosition.TOP
        )

        self.addSubInterface(
            self.advanced_page, FIF.ROBOT, "Advanced",
            NavigationItemPosition.TOP
        )

    def _init_theme_action(self):
        self.navigationInterface.addItem(
            routeKey="theme_toggle",
            icon=FIF.CONSTRACT,
            text="Toggle Theme",
            onClick=self._toggle_theme,
            position=NavigationItemPosition.BOTTOM,
        )

        self._theme_manager.themeChanged.connect(self._on_theme_changed)

    def _toggle_theme(self):
        self._theme_manager.toggle_theme()

    def _on_theme_changed(self, theme):
        pages = [
            self.hero_page,
            self.basic_widgets_page,
            self.input_widgets_page,
            self.navigation_widgets_page,
            self.feedback_widgets_page,
            self.data_widgets_page,
            self.layout_widgets_page,
            self.custom_widgets_page,
            self.charts_page,
            self.diagrams_page,
            self.social_page,
            self.media_page,
            self.form_enhanced_page,
            self.status_page,
            self.advanced_page,
        ]
        for page in pages:
            if page is not None:
                if page.isVisible():
                    if hasattr(page, 'refresh_theme'):
                        page.refresh_theme()
                else:
                    if hasattr(page, 'mark_theme_stale'):
                        page.mark_theme_stale()
