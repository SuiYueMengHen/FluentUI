from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ConnectionStatus(QWidget):
    def __init__(self, connected=True, label="", parent=None):
        super().__init__(parent)
        self._connected = connected
        self._label = label
        self._pulse_scale = 1.0
        self._pulse_opacity = 1.0
        self._pulse_running = True
        self.setFixedHeight(28)
        self._pulse_anim = QPropertyAnimation(self, b"pulseScale")
        self._pulse_anim.setDuration(1500)
        self._pulse_anim.setStartValue(1.0)
        self._pulse_anim.setEndValue(2.0)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        if self._connected and self._pulse_running:
            self._pulse_anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._pulse_anim.stop()

    def get_pulse_scale(self):
        return self._pulse_scale

    def set_pulse_scale(self, val):
        self._pulse_scale = val
        self._pulse_opacity = max(0.0, 1.0 - (val - 1.0))
        self.update()

    pulseScale = Property(float, get_pulse_scale, set_pulse_scale)

    def set_connected(self, connected):
        self._connected = connected
        self.update()

    def set_label(self, label):
        self._label = label
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        dot_color = QColor("#0F7B0F") if self._connected else QColor("#C42B1C")
        cx = 14
        cy = self.height() / 2
        dot_r = 5
        pulse_r = dot_r * self._pulse_scale
        pulse_color = QColor(dot_color)
        pulse_color.setAlpha(int(80 * self._pulse_opacity))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(pulse_color)
        painter.drawEllipse(QRectF(cx - pulse_r, cy - pulse_r, pulse_r * 2, pulse_r * 2))
        painter.setBrush(dot_color)
        painter.drawEllipse(QRectF(cx - dot_r, cy - dot_r, dot_r * 2, dot_r * 2))
        if self._label:
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(QRectF(30, 0, self.width() - 30, self.height()), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._label)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
