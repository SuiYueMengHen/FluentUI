from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QSettings
from qfluentwidgets import Theme, setTheme, isDarkTheme, setThemeColor


class ThemeManager(QObject):
    themeChanged = Signal(Theme)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        super().__init__()
        self._initialized = True
        self._settings = QSettings("FluentUI", "Gallery")
        self._accent_color = "#0078D4"
        setThemeColor(self._accent_color)

    @property
    def current_theme(self):
        theme_str = self._settings.value("theme", "auto")
        if theme_str == "light":
            return Theme.LIGHT
        elif theme_str == "dark":
            return Theme.DARK
        else:
            return Theme.AUTO

    def set_theme(self, theme: Theme):
        setTheme(theme)
        theme_str = {Theme.LIGHT: "light", Theme.DARK: "dark", Theme.AUTO: "auto"}.get(
            theme, "auto"
        )
        self._settings.setValue("theme", theme_str)
        self.themeChanged.emit(theme)

    def toggle_theme(self):
        if isDarkTheme():
            self.set_theme(Theme.LIGHT)
        else:
            self.set_theme(Theme.DARK)

    def is_dark(self):
        return isDarkTheme()

    @property
    def accent_color(self):
        return self._accent_color

    @accent_color.setter
    def accent_color(self, color: str):
        self._accent_color = color
        setThemeColor(color)

    def get_color(self, token: str):
        colors_light = {
            "primary": "#0067C0",
            "background": "#F3F3F3",
            "surface": "#FFFFFF",
            "text_primary": "#1A1A1A",
            "text_secondary": "#616161",
            "accent": "#0078D4",
            "error": "#C42B1C",
            "success": "#0F7B0F",
            "warning": "#9D5D00",
            "border": "#E5E5E5",
        }
        colors_dark = {
            "primary": "#60CDFF",
            "background": "#202020",
            "surface": "#2D2D2D",
            "text_primary": "#FFFFFF",
            "text_secondary": "#9E9E9E",
            "accent": "#0078D4",
            "error": "#FF6B6B",
            "success": "#6CCB5F",
            "warning": "#FFB900",
            "border": "#3D3D3D",
        }
        palette = colors_dark if self.is_dark() else colors_light
        return palette.get(token, "#000000")
