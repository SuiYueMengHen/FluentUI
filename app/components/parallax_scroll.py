from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ParallaxScroll(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scroll_offset = 0.0
        self._layers = [
            {"color": "#0078D4", "speed": 0.3, "y_offset": 0},
            {"color": "#005A9E", "speed": 0.6, "y_offset": 40},
            {"color": "#003D6B", "speed": 1.0, "y_offset": 80},
        ]
        self.setFixedWidth(300)
        self.setMinimumHeight(300)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._auto_scroll)

    def showEvent(self, event):
        super().showEvent(event)
        self._timer.start(30)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def _auto_scroll(self):
        self._scroll_offset += 0.5
        self.update()

    def wheelEvent(self, event):
        self._scroll_offset += event.angleDelta().y() * 0.5
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#1A1A1A") if dark else QColor("#F0F0F0")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
        for layer in self._layers:
            speed = layer["speed"]
            color = QColor(layer["color"])
            if dark:
                color = color.lighter(130)
            y_base = layer["y_offset"]
            offset = (self._scroll_offset * speed) % (self.height() + 60) - 30
            block_h = 60
            block_w = self.width() - 40
            for rep in range(-1, 4):
                y = y_base + rep * (block_h + 30) + offset
                if -block_h <= y <= self.height():
                    color_copy = QColor(color)
                    color_copy.setAlpha(60)
                    painter.setBrush(color_copy)
                    painter.drawRoundedRect(QRectF(20, y, block_w, block_h), 10, 10)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
