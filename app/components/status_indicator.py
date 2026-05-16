from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush


class StatusIndicator(QWidget):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    AWAY = "away"

    STATUS_COLORS = {
        "online": "#6CCB5F",
        "offline": "#9E9E9E",
        "busy": "#FF6B6B",
        "away": "#FFB900",
    }

    def __init__(self, status="online", size=12, parent=None):
        super().__init__(parent)
        self._status = status
        self._dot_size = size
        self._pulse_scale = 1.0
        self._breathing = True

        self.setFixedSize(size + 8, size + 8)

        self._breath_timer = QTimer(self)
        self._breath_timer.timeout.connect(self._breath_tick)

        self._breath_phase = 0.0

    def showEvent(self, event):
        super().showEvent(event)
        self._breath_timer.start(50)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._breath_timer.stop()

    def _breath_tick(self):
        if not self._breathing:
            return
        self._breath_phase += 0.05
        self._pulse_scale = 1.0 + 0.15 * abs((self._breath_phase % (2 * 3.14159)) / 3.14159 - 1)
        self.update()

    def set_status(self, status: str):
        self._status = status
        self.update()

    def set_breathing(self, enabled: bool):
        self._breathing = enabled
        if not enabled:
            self._pulse_scale = 1.0
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(self.STATUS_COLORS.get(self._status, "#9E9E9E"))
        center_x = self.width() / 2
        center_y = self.height() / 2
        base_r = self._dot_size / 2

        glow_r = base_r * self._pulse_scale * 1.8
        glow_color = QColor(color)
        glow_color.setAlpha(40)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow_color)
        painter.drawEllipse(QRectF(center_x - glow_r, center_y - glow_r, glow_r * 2, glow_r * 2))

        painter.setBrush(color)
        painter.drawEllipse(QRectF(center_x - base_r, center_y - base_r, base_r * 2, base_r * 2))

        highlight_r = base_r * 0.35
        highlight_color = QColor(255, 255, 255, 120)
        painter.setBrush(highlight_color)
        painter.drawEllipse(QRectF(center_x - base_r * 0.3, center_y - base_r * 0.3, highlight_r * 2, highlight_r * 2))

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
