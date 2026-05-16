from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class GlassCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        self._blur_progress = 1.0
        self.setFixedSize(240, 160)
        self._anim = QPropertyAnimation(self, b"blurProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_blur_progress(self):
        return self._blur_progress

    def set_blur_progress(self, val):
        self._blur_progress = val
        self.update()

    blurProgress = Property(float, get_blur_progress, set_blur_progress)

    def set_title(self, title):
        self._title = title
        self.update()

    def enterEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._blur_progress)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._blur_progress)
        self._anim.setEndValue(0.6)
        self._anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        border_color = QColor("#505050") if dark else QColor("#D0D0D0")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        if dark:
            glass_color = QColor(255, 255, 255, int(25 * self._blur_progress))
        else:
            glass_color = QColor(255, 255, 255, int(50 * self._blur_progress))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glass_color)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 255, 255, int(30 * self._blur_progress)))
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
