import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class PieChart(QWidget):
    def __init__(self, data=None, labels=None, colors=None, donut=False, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._labels = labels or []
        self._colors = colors or []
        self._donut = donut
        self._sweep_progress = 0.0
        self.setMinimumSize(200, 200)

        self._anim = QPropertyAnimation(self, b"_sweep_progress_prop")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_sweep_progress(self):
        return self._sweep_progress

    def set_sweep_progress(self, val):
        self._sweep_progress = val
        self.update()

    _sweep_progress_prop = Property(float, get_sweep_progress, set_sweep_progress)

    def _is_dark(self):
        return isDarkTheme()

    def refresh_theme(self):
        self.update()
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        label_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
        value_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

        w = self.width()
        h = self.height()

        if not self._data:
            painter.end()
            return

        total = sum(self._data)
        if total == 0:
            painter.end()
            return

        side = min(w, h)
        cx = w / 2
        cy = h / 2
        radius = side / 2 - 50
        if radius < 20:
            radius = 20
        inner_radius = radius * 0.55 if self._donut else 0

        default_colors = ["#0078D4", "#00B4D8", "#6CCB5F", "#FFB900", "#FF6B6B", "#B4A0FF", "#FF8C42", "#4ECDC4"]
        gap_angle = 1.0

        start_angle = 90.0
        font = QFont()
        font.setPixelSize(11)
        painter.setFont(font)

        for i, val in enumerate(self._data):
            if i < len(self._colors):
                color = QColor(self._colors[i])
            else:
                color = QColor(default_colors[i % len(default_colors)])

            sweep = (val / total) * 360.0 * self._sweep_progress
            actual_sweep = max(0, sweep - gap_angle)
            if actual_sweep <= 0:
                start_angle += sweep
                continue

            path = QPainterPath()
            rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
            start_qt = start_angle * 16
            span_qt = -actual_sweep * 16

            if self._donut and inner_radius > 0:
                inner_rect = QRectF(cx - inner_radius, cy - inner_radius, inner_radius * 2, inner_radius * 2)
                path.arcMoveTo(rect, start_angle)
                path.arcTo(rect, start_angle, -actual_sweep)
                path.arcTo(inner_rect, start_angle - actual_sweep, actual_sweep)
                path.closeSubpath()
            else:
                path.moveTo(cx, cy)
                path.arcTo(rect, start_angle, -actual_sweep)
                path.closeSubpath()

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawPath(path)

            if self._sweep_progress > 0.8 and i < len(self._labels):
                mid_angle = start_angle - sweep / 2
                mid_rad = math.radians(mid_angle)
                label_r = radius + 20
                lx = cx + label_r * math.cos(mid_rad)
                ly = cy - label_r * math.sin(mid_rad)

                line_start_r = radius + 3
                line_end_r = radius + 14
                lsx = cx + line_start_r * math.cos(mid_rad)
                lsy = cy - line_start_r * math.sin(mid_rad)
                lex = cx + line_end_r * math.cos(mid_rad)
                ley = cy - line_end_r * math.sin(mid_rad)

                line_pen = QPen(label_color, 1)
                painter.setPen(line_pen)
                painter.drawLine(QPointF(lsx, lsy), QPointF(lex, ley))

                text_r = radius + 20
                tx = cx + text_r * math.cos(mid_rad)
                ty = cy - text_r * math.sin(mid_rad)
                painter.setPen(label_color)
                text_rect = QRectF(tx - 50, ty - 10, 100, 20)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._labels[i])

            start_angle += sweep

        if self._donut and inner_radius > 0 and self._sweep_progress > 0.5:
            painter.setPen(value_color)
            font.setPixelSize(18)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(QRectF(cx - inner_radius, cy - 12, inner_radius * 2, 24), Qt.AlignmentFlag.AlignCenter, f"{total:.0f}")

        painter.end()
