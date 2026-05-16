import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QLinearGradient
from qfluentwidgets import isDarkTheme


class WaveProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0
        self._wave_offset = 0.0

        self.setFixedSize(200, 120)

        self._wave_timer = QTimer(self)
        self._wave_timer.timeout.connect(self._wave_tick)

        self._value_anim = QPropertyAnimation(self, b"displayValue")
        self._value_anim.setDuration(600)
        self._value_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self._wave_timer.start(30)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._wave_timer.stop()

    def _is_dark(self):
        return isDarkTheme()

    def get_display_value(self):
        return self._display_value

    def set_display_value(self, val):
        self._display_value = val
        self.update()

    displayValue = Property(float, get_display_value, set_display_value)

    def _wave_tick(self):
        self._wave_offset += 0.06
        if self._wave_offset > 2 * math.pi:
            self._wave_offset -= 2 * math.pi
        self.update()

    def set_value(self, value):
        self._value = max(0, min(100, value))
        self._value_anim.setStartValue(self._display_value)
        self._value_anim.setEndValue(float(self._value))
        self._value_anim.start()

    def get_value(self):
        return self._value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg_color = QColor("#2D2D2D") if is_dark else QColor("#F0F0F0")
        wave_base = QColor("#60CDFF") if is_dark else QColor("#0078D4")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

        w = self.width()
        h = self.height()
        border_r = 12

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(QRectF(0, 0, w, h), border_r, border_r)

        clip_path = QPainterPath()
        clip_path.addRoundedRect(QRectF(0, 0, w, h), border_r, border_r)
        painter.setClipPath(clip_path)

        water_level = h - (self._display_value / 100.0) * h

        wave1_color = QColor(wave_base)
        wave1_color.setAlpha(100)
        path1 = QPainterPath()
        path1.moveTo(0, h)
        for x in range(w + 1):
            y = water_level + 6 * math.sin((x / w) * 2 * math.pi * 2 + self._wave_offset)
            path1.lineTo(x, y)
        path1.lineTo(w, h)
        path1.closeSubpath()
        painter.setBrush(wave1_color)
        painter.drawPath(path1)

        wave2_color = QColor(wave_base)
        wave2_color.setAlpha(180)
        path2 = QPainterPath()
        path2.moveTo(0, h)
        for x in range(w + 1):
            y = water_level + 4 * math.sin((x / w) * 2 * math.pi * 2 + self._wave_offset * 1.5 + 1.5)
            path2.lineTo(x, y)
        path2.lineTo(w, h)
        path2.closeSubpath()
        painter.setBrush(wave2_color)
        painter.drawPath(path2)

        painter.setClipping(False)

        painter.setPen(text_color)
        font = QFont()
        font.setPixelSize(28)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            QRectF(0, 0, w, h),
            Qt.AlignmentFlag.AlignCenter,
            f"{int(self._display_value)}%"
        )

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
