import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class RadarChart(QWidget):
    def __init__(self, categories=None, series=None, parent=None):
        super().__init__(parent)
        self._categories = categories or []
        self._series = series or []
        self._scale_progress = 0.0
        self.setMinimumSize(200, 200)

        self._anim = QPropertyAnimation(self, b"_scale_progress_prop")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_scale_progress(self):
        return self._scale_progress

    def set_scale_progress(self, val):
        self._scale_progress = val
        self.update()

    _scale_progress_prop = Property(float, get_scale_progress, set_scale_progress)

    def _is_dark(self):
        return isDarkTheme()

    def refresh_theme(self):
        self.update()
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        grid_color = QColor("#404040") if is_dark else QColor("#E0E0E0")
        axis_color = QColor("#505050") if is_dark else QColor("#BDBDBD")
        label_color = QColor("#9E9E9E") if is_dark else QColor("#616161")

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2
        radius = min(w, h) / 2 - 40
        if radius < 20:
            radius = 20

        n = len(self._categories)
        if n < 3:
            painter.end()
            return

        angle_step = 360.0 / n
        levels = 5

        for level in range(1, levels + 1):
            r = radius * level / levels
            path = QPainterPath()
            for i in range(n):
                angle = math.radians(90 - i * angle_step)
                px = cx + r * math.cos(angle)
                py = cy - r * math.sin(angle)
                if i == 0:
                    path.moveTo(px, py)
                else:
                    path.lineTo(px, py)
            path.closeSubpath()
            pen = QPen(grid_color, 1)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

        for i in range(n):
            angle = math.radians(90 - i * angle_step)
            ex = cx + radius * math.cos(angle)
            ey = cy - radius * math.sin(angle)
            pen = QPen(axis_color, 1)
            painter.setPen(pen)
            painter.drawLine(QPointF(cx, cy), QPointF(ex, ey))

            font = QFont()
            font.setPixelSize(11)
            painter.setFont(font)
            painter.setPen(label_color)
            label_r = radius + 16
            lx = cx + label_r * math.cos(angle)
            ly = cy - label_r * math.sin(angle)
            text_rect = QRectF(lx - 40, ly - 10, 80, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._categories[i])

        default_colors = ["#0078D4", "#00B4D8", "#6CCB5F", "#FFB900", "#FF6B6B"]
        for si, s in enumerate(self._series):
            data = s.get("data", [])
            color = QColor(s.get("color", default_colors[si % len(default_colors)]))
            if len(data) != n:
                continue

            path = QPainterPath()
            for i in range(n):
                val = data[i]
                r = (val / 100.0) * radius * self._scale_progress
                angle = math.radians(90 - i * angle_step)
                px = cx + r * math.cos(angle)
                py = cy - r * math.sin(angle)
                if i == 0:
                    path.moveTo(px, py)
                else:
                    path.lineTo(px, py)
            path.closeSubpath()

            fill_color = QColor(color)
            fill_color.setAlpha(50)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(fill_color))
            painter.drawPath(path)

            pen = QPen(color, 2)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

            for i in range(n):
                val = data[i]
                r = (val / 100.0) * radius * self._scale_progress
                angle = math.radians(90 - i * angle_step)
                px = cx + r * math.cos(angle)
                py = cy - r * math.sin(angle)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawEllipse(QPointF(px, py), 3, 3)

        painter.end()
