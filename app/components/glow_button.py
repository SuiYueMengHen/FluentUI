from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen


class GlowButton(QPushButton):
    def __init__(self, text="", parent=None, accent_color="#0078D4"):
        super().__init__(text, parent)
        self._accent_color = accent_color
        self._glow_intensity = 0.0
        self._border_radius = 8
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._glow_anim = QPropertyAnimation(self, b"glowIntensity")
        self._glow_anim.setDuration(200)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_glow_intensity(self):
        return self._glow_intensity

    def set_glow_intensity(self, val):
        self._glow_intensity = val
        self.update()

    glowIntensity = Property(float, get_glow_intensity, set_glow_intensity)

    def enterEvent(self, event):
        self._glow_anim.setStartValue(self._glow_intensity)
        self._glow_anim.setEndValue(1.0)
        self._glow_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._glow_anim.setStartValue(self._glow_intensity)
        self._glow_anim.setEndValue(0.0)
        self._glow_anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        accent = QColor(self._accent_color)
        glow_alpha = int(self._glow_intensity * 60)

        if self.isDown():
            bg_color = accent.darker(120)
        else:
            bg_color = accent

        if self._glow_intensity > 0:
            glow_color = QColor(accent)
            glow_color.setAlpha(glow_alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow_color)
            painter.drawRoundedRect(self.rect().adjusted(-4, -4, 4, 4), self._border_radius + 4, self._border_radius + 4)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(self.rect(), self._border_radius, self._border_radius)

        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
