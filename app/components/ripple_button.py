from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF, QObject
from PySide6.QtGui import QPainter, QColor, QPen, QPalette, QPainterPath
from qfluentwidgets import isDarkTheme


class _Ripple(QObject):
    def __init__(self, position, max_radius, button):
        super().__init__(button)
        self.position = position
        self.max_radius = max_radius
        self._radius = 0.0
        self._opacity = 0.3
        self._button = button

        self._radius_anim = QPropertyAnimation(self, b"rippleRadius")
        self._radius_anim.setDuration(300)
        self._radius_anim.setStartValue(0.0)
        self._radius_anim.setEndValue(max_radius)
        self._radius_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._opacity_anim = QPropertyAnimation(self, b"rippleOpacity")
        self._opacity_anim.setDuration(300)
        self._opacity_anim.setStartValue(0.3)
        self._opacity_anim.setEndValue(0.0)
        self._opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._radius_anim.start()
        self._opacity_anim.start()

        self._opacity_anim.finished.connect(self._on_finished)

    def get_ripple_radius(self):
        return self._radius

    def set_ripple_radius(self, val):
        self._radius = val
        self._button.update()

    rippleRadius = Property(float, get_ripple_radius, set_ripple_radius)

    def get_ripple_opacity(self):
        return self._opacity

    def set_ripple_opacity(self, val):
        self._opacity = val
        self._button.update()

    rippleOpacity = Property(float, get_ripple_opacity, set_ripple_opacity)

    def _on_finished(self):
        try:
            if self in self._button._ripples:
                self._button._ripples.remove(self)
        except RuntimeError:
            pass
        self.deleteLater()


class RippleButton(QPushButton):
    def __init__(self, text="", parent=None, accent_color="#0078D4"):
        super().__init__(text, parent)
        self._accent_color = accent_color
        self._scale_factor = 1.0
        self._ripples = []
        self._border_radius = 8

        self.setMinimumHeight(44)
        self.setMinimumWidth(100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._scale_anim = QPropertyAnimation(self, b"scaleFactor")
        self._scale_anim.setDuration(150)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.refresh_theme()

    def get_scale_factor(self):
        return self._scale_factor

    def set_scale_factor(self, val):
        self._scale_factor = val
        self.update()

    scaleFactor = Property(float, get_scale_factor, set_scale_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            max_radius = (self.width() ** 2 + self.height() ** 2) ** 0.5
            ripple = _Ripple(pos, max_radius, self)
            self._ripples.append(ripple)

            self._scale_anim.stop()
            self._scale_anim.setStartValue(self._scale_factor)
            self._scale_anim.setEndValue(0.97)
            self._scale_anim.start()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._scale_anim.stop()
            self._scale_anim.setStartValue(self._scale_factor)
            self._scale_anim.setEndValue(1.0)
            self._scale_anim.start()

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        painter.translate(w / 2, h / 2)
        painter.scale(self._scale_factor, self._scale_factor)
        painter.translate(-w / 2, -h / 2)

        clip_path = QPainterPath()
        clip_path.addRoundedRect(QRectF(self.rect()), self._border_radius, self._border_radius)
        painter.setClipPath(clip_path)

        accent = QColor(self._accent_color)
        if self.isEnabled():
            bg = accent
        else:
            bg = accent.darker(150)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(self.rect()), self._border_radius, self._border_radius)

        for ripple in self._ripples:
            alpha = int(ripple._opacity * 255)
            ripple_color = QColor(255, 255, 255, alpha)
            painter.setBrush(ripple_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(
                ripple.position.x() - ripple._radius,
                ripple.position.y() - ripple._radius,
                ripple._radius * 2,
                ripple._radius * 2
            ))

        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
