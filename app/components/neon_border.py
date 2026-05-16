from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QRadialGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class NeonBorder(QWidget):
    def __init__(self, color="#0078D4", parent=None):
        super().__init__(parent)
        self._color = color
        self._glow_intensity = 0.5
        self._pulse_up = True
        self.setFixedSize(200, 120)
        self._anim = QPropertyAnimation(self, b"glowIntensity")
        self._anim.setDuration(1500)
        self._anim.setStartValue(0.5)
        self._anim.setEndValue(1.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self._anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._anim.stop()

    def get_glow_intensity(self):
        return self._glow_intensity

    def set_glow_intensity(self, val):
        self._glow_intensity = val
        self.update()

    glowIntensity = Property(float, get_glow_intensity, set_glow_intensity)

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        neon_color = QColor(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        for i in range(4):
            glow = QColor(neon_color)
            alpha = int(30 * self._glow_intensity * (4 - i) / 4)
            glow.setAlpha(alpha)
            offset = (4 - i) * 3
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow)
            painter.drawRoundedRect(QRectF(-offset, -offset, self.width() + offset * 2, self.height() + offset * 2), 12 + offset, 12 + offset)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(4, 4, self.width() - 8, self.height() - 8), 10, 10)
        pen = QPen(neon_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(4, 4, self.width() - 8, self.height() - 8), 10, 10)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
