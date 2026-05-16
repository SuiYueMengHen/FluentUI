import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QConicalGradient, QRadialGradient
from qfluentwidgets import isDarkTheme


class GaugeChart(QWidget):
    def __init__(self, value=0, min_val=0, max_val=100, label="", parent=None):
        super().__init__(parent)
        self._value = value
        self._min_val = min_val
        self._max_val = max_val
        self._label = label
        self._needle_angle = 0.0
        self.setMinimumSize(160, 120)

        self._anim = QPropertyAnimation(self, b"_needle_angle_prop")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._set_needle_target(value)

    def _set_needle_target(self, value):
        clamped = max(self._min_val, min(self._max_val, value))
        ratio = (clamped - self._min_val) / (self._max_val - self._min_val) if self._max_val != self._min_val else 0
        target = -135 + ratio * 270
        self._anim.setStartValue(self._needle_angle)
        self._anim.setEndValue(target)
        self._anim.start()

    def get_needle_angle(self):
        return self._needle_angle

    def set_needle_angle(self, val):
        self._needle_angle = val
        self.update()

    _needle_angle_prop = Property(float, get_needle_angle, set_needle_angle)

    def _is_dark(self):
        return isDarkTheme()

    def set_value(self, value):
        self._value = value
        self._set_needle_target(value)

    def refresh_theme(self):
        self.update()
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg_arc_color = QColor("#404040") if is_dark else QColor("#E0E0E0")
        value_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        tick_color = QColor("#606060") if is_dark else QColor("#9E9E9E")
        label_color = QColor("#9E9E9E") if is_dark else QColor("#616161")

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h * 0.6
        radius = min(w, h) * 0.42
        if radius < 20:
            radius = 20

        stroke = max(8, radius * 0.12)

        bg_rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
        bg_pen = QPen(bg_arc_color, stroke)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(bg_rect, 135 * 16, -270 * 16)

        ratio = (self._value - self._min_val) / (self._max_val - self._min_val) if self._max_val != self._min_val else 0
        ratio = max(0, min(1, ratio))

        if ratio > 0.6:
            arc_color = QColor("#FF6B6B")
        elif ratio > 0.3:
            arc_color = QColor("#FFB900")
        else:
            arc_color = QColor("#0078D4")

        value_pen = QPen(arc_color, stroke)
        value_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(value_pen)
        span = -ratio * 270 * 16
        painter.drawArc(bg_rect, 135 * 16, int(span))

        tick_count = 10
        for i in range(tick_count + 1):
            angle_deg = 135 - i * (270 / tick_count)
            angle_rad = math.radians(angle_deg)
            inner_r = radius - stroke / 2 - 6
            outer_r = radius - stroke / 2 - 2
            x1 = cx + inner_r * math.cos(angle_rad)
            y1 = cy - inner_r * math.sin(angle_rad)
            x2 = cx + outer_r * math.cos(angle_rad)
            y2 = cy - outer_r * math.sin(angle_rad)
            tick_pen = QPen(tick_color, 1.5)
            painter.setPen(tick_pen)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        needle_rad = math.radians(self._needle_angle)
        needle_len = radius - stroke / 2 - 10
        nx = cx + needle_len * math.cos(needle_rad)
        ny = cy - needle_len * math.sin(needle_rad)

        needle_pen = QPen(arc_color, 2.5)
        needle_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(needle_pen)
        painter.drawLine(QPointF(cx, cy), QPointF(nx, ny))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(arc_color))
        painter.drawEllipse(QPointF(cx, cy), 5, 5)

        font = QFont()
        font.setPixelSize(max(14, int(radius * 0.3)))
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(value_color)
        painter.drawText(QRectF(cx - radius, cy + 10, radius * 2, 30), Qt.AlignmentFlag.AlignCenter, f"{self._value:.0f}")

        if self._label:
            font.setPixelSize(11)
            font.setBold(False)
            painter.setFont(font)
            painter.setPen(label_color)
            painter.drawText(QRectF(cx - radius, cy + 36, radius * 2, 20), Qt.AlignmentFlag.AlignCenter, self._label)

        painter.end()
