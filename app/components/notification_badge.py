from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont


class NotificationBadge(QWidget):
    def __init__(self, count=0, parent=None, color="#FF4444"):
        super().__init__(parent)
        self._count = count
        self._color = color
        self._pulse_scale = 1.0

        self.setFixedSize(24, 24)

        self._pulse_anim = QPropertyAnimation(self, b"pulseScale")
        self._pulse_anim.setDuration(300)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._pulse_anim.setLoopCount(3)

    def _is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def get_pulse_scale(self):
        return self._pulse_scale

    def set_pulse_scale(self, val):
        self._pulse_scale = val
        self.update()

    pulseScale = Property(float, get_pulse_scale, set_pulse_scale)

    def set_count(self, count):
        self._count = count
        self._pulse_anim.setStartValue(1.0)
        self._pulse_anim.setKeyValueAt(0.5, 1.2)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.start()
        self.update()

    def get_count(self):
        return self._count

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2
        base_r = 12

        scaled_r = base_r * self._pulse_scale

        bg_color = QColor(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawEllipse(QRectF(
            center_x - scaled_r,
            center_y - scaled_r,
            scaled_r * 2,
            scaled_r * 2
        ))

        if self._count > 0:
            painter.setPen(QColor("#FFFFFF"))
            font = QFont()
            font.setPixelSize(11)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(
                QRectF(0, 0, self.width(), self.height()),
                Qt.AlignmentFlag.AlignCenter,
                str(self._count)
            )

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
