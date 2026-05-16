from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QConicalGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class AnimatedBorder(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        self._rotation = 0.0
        self.setFixedSize(200, 120)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def showEvent(self, event):
        super().showEvent(event)
        self._timer.start(16)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def _tick(self):
        self._rotation = (self._rotation + 1.2) % 360
        self.update()

    def set_title(self, title):
        self._title = title
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        inner_bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2
        border_w = 3
        outer_r = min(w, h) / 2
        gradient = QConicalGradient(cx, cy, self._rotation)
        gradient.setColorAt(0, QColor("#0078D4"))
        gradient.setColorAt(0.25, QColor("#60CDFF"))
        gradient.setColorAt(0.5, QColor("#0078D4"))
        gradient.setColorAt(0.75, QColor("#60CDFF"))
        gradient.setColorAt(1, QColor("#0078D4"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(QRectF(0, 0, w, h), 12, 12)
        painter.setBrush(inner_bg)
        painter.drawRoundedRect(QRectF(border_w, border_w, w - border_w * 2, h - border_w * 2), 10, 10)
        if self._title:
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            painter.setFont(font)
            inner_rect = QRectF(border_w, border_w, w - border_w * 2, h - border_w * 2)
            painter.drawText(inner_rect, Qt.AlignmentFlag.AlignCenter, self._title)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
