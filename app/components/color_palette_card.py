from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor


class ColorSwatch(QFrame):
    clicked = Signal(str)

    def __init__(self, color_name: str, color_hex: str, parent=None):
        super().__init__(parent)
        self._color_name = color_name
        self._color_hex = color_hex
        self.setFixedSize(48, 48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"{color_name}\n{color_hex}\nClick to copy")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self._color_hex))
        painter.drawRoundedRect(self.rect(), 8, 8)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            clipboard = QApplication.clipboard()
            clipboard.setText(self._color_hex)
            self.clicked.emit(self._color_hex)
        super().mousePressEvent(event)


class ColorPaletteCard(QFrame):
    colorCopied = Signal(str)

    def __init__(self, title="Color Palette", colors=None, parent=None):
        super().__init__(parent)
        self._title = title
        self.setObjectName("colorPaletteCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)

        title_label = QLabel(title, self)
        self._title_label = title_label
        self._update_title_style()
        layout.addWidget(title_label)

        swatch_layout = QHBoxLayout()
        swatch_layout.setSpacing(8)

        if colors is None:
            colors = [
                ("Primary", "#0078D4"),
                ("Secondary", "#616161"),
                ("Accent", "#60CDFF"),
                ("Success", "#6CCB5F"),
                ("Warning", "#FFB900"),
                ("Error", "#FF6B6B"),
            ]

        for name, hex_color in colors:
            swatch = ColorSwatch(name, hex_color, self)
            swatch.clicked.connect(self.colorCopied.emit)
            swatch_layout.addWidget(swatch)

        swatch_layout.addStretch()
        layout.addLayout(swatch_layout)

    def _update_title_style(self):
        from qfluentwidgets import isDarkTheme
        color = "#1A1A1A" if not isDarkTheme() else "#FFFFFF"
        self._title_label.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {color}; background: transparent;")

    def paintEvent(self, event):
        from qfluentwidgets import isDarkTheme
        is_dark = isDarkTheme()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(255, 255, 255, 13) if is_dark else QColor(0, 0, 0, 8)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 12, 12)

        border = QColor(255, 255, 255, 20) if is_dark else QColor(0, 0, 0, 20)
        painter.setPen(border)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 11, 11)

        painter.end()
        super().paintEvent(event)

    def refresh_theme(self):
        self._update_title_style()
        self.update()
        self.repaint()
