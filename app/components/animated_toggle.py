from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen


class AnimatedToggle(QWidget):
    def __init__(self, parent=None, on_color="#0078D4", off_color=None):
        super().__init__(parent)
        self._checked = False
        self._on_color = on_color
        self._off_color = off_color
        self._thumb_position = 0.0

        self.setFixedSize(48, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"thumbPosition")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutElastic)

    def _is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def get_thumb_position(self):
        return self._thumb_position

    def set_thumb_position(self, val):
        self._thumb_position = val
        self.update()

    thumbPosition = Property(float, get_thumb_position, set_thumb_position)

    def is_checked(self):
        return self._checked

    def set_checked(self, checked, animate=True):
        self._checked = checked
        if animate:
            self._anim.setStartValue(self._thumb_position)
            self._anim.setEndValue(1.0 if checked else 0.0)
            self._anim.start()
        else:
            self._thumb_position = 1.0 if checked else 0.0
            self.update()

    def get_on_color(self):
        return self._on_color

    def set_on_color(self, color):
        self._on_color = color
        self.update()

    def get_off_color(self):
        return self._off_color

    def set_off_color(self, color):
        self._off_color = color
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_checked(not self._checked)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()

        if self._checked:
            track_color = QColor(self._on_color)
        else:
            if self._off_color:
                track_color = QColor(self._off_color)
            else:
                track_color = QColor("#3D3D3D") if is_dark else QColor("#E0E0E0")

        track_rect = QRectF(0, 0, 48, 24)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, 12, 12)

        thumb_margin = 2
        thumb_diameter = 20
        thumb_x = thumb_margin + self._thumb_position * (48 - thumb_diameter - thumb_margin * 2)
        thumb_y = (24 - thumb_diameter) / 2

        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(QRectF(thumb_x, thumb_y, thumb_diameter, thumb_diameter))

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
