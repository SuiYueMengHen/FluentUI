from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class SpotlightCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        self._spotlight_x = -1.0
        self._spotlight_y = -1.0
        self.setFixedSize(240, 160)
        self.setMouseTracking(True)

    def set_title(self, title):
        self._title = title
        self.update()

    def mouseMoveEvent(self, event):
        self._spotlight_x = event.position().x()
        self._spotlight_y = event.position().y()
        self.update()

    def leaveEvent(self, event):
        self._spotlight_x = -1.0
        self._spotlight_y = -1.0
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border_color = QColor("#505050") if dark else QColor("#D0D0D0")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        if self._spotlight_x >= 0 and self._spotlight_y >= 0:
            gradient = QRadialGradient(QPointF(self._spotlight_x, self._spotlight_y), 120)
            gradient.setColorAt(0, QColor(255, 255, 255, 30))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(gradient)
            painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        pen = QPen(border_color, 1)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        if self._title:
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(QRectF(16, 16, self.width() - 32, 24), Qt.AlignmentFlag.AlignLeft, self._title)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
