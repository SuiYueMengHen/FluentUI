from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QPainterPath
from qfluentwidgets import isDarkTheme


class AreaChart(QWidget):
    def __init__(self, series=None, labels=None, parent=None):
        super().__init__(parent)
        self._series = series or []
        self._labels = labels or []
        self._fill_progress = 0.0
        self.setMinimumSize(200, 150)

        self._anim = QPropertyAnimation(self, b"_fill_progress_prop")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_fill_progress(self):
        return self._fill_progress

    def set_fill_progress(self, val):
        self._fill_progress = val
        self.update()

    _fill_progress_prop = Property(float, get_fill_progress, set_fill_progress)

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
        axis_text_color = QColor("#9E9E9E") if is_dark else QColor("#616161")

        w = self.width()
        h = self.height()
        margin_left = 50
        margin_right = 20
        margin_top = 30
        margin_bottom = 40

        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if not self._series or chart_w <= 0 or chart_h <= 0:
            painter.end()
            return

        all_vals = []
        for s in self._series:
            all_vals.extend(s.get("data", []))
        if not all_vals:
            painter.end()
            return

        max_val = max(all_vals)
        min_val = min(0, min(all_vals))
        val_range = max_val - min_val if max_val != min_val else 1

        grid_pen = QPen(grid_color, 1, Qt.PenStyle.DashLine)
        painter.setPen(grid_pen)
        grid_count = 5
        for i in range(grid_count + 1):
            y = margin_top + chart_h - (i / grid_count) * chart_h
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))

        axis_pen = QPen(axis_text_color, 1)
        painter.setPen(axis_pen)
        painter.drawLine(int(margin_left), int(margin_top), int(margin_left), int(margin_top + chart_h))
        painter.drawLine(int(margin_left), int(margin_top + chart_h), int(w - margin_right), int(margin_top + chart_h))

        font = QFont()
        font.setPixelSize(11)
        painter.setFont(font)
        painter.setPen(axis_text_color)
        for i in range(grid_count + 1):
            y = margin_top + chart_h - (i / grid_count) * chart_h
            val = min_val + val_range * i / grid_count
            painter.drawText(QRectF(0, y - 10, margin_left - 5, 20), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{val:.0f}")

        if self._labels:
            max_points = max(len(s.get("data", [])) for s in self._series) if self._series else 0
            step = chart_w / (max(len(self._labels) - 1, 1))
            painter.setPen(axis_text_color)
            font.setPixelSize(11)
            painter.setFont(font)
            for i, lbl in enumerate(self._labels):
                x = margin_left + i * step
                painter.drawText(QRectF(x - 30, margin_top + chart_h + 5, 60, 30), Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop, lbl)

        for s in self._series:
            data = s.get("data", [])
            color = QColor(s.get("color", "#0078D4"))
            if not data:
                continue

            step = chart_w / (len(data) - 1) if len(data) > 1 else chart_w
            points = []
            for i, val in enumerate(data):
                x = margin_left + i * step
                y = margin_top + chart_h - ((val - min_val) / val_range) * chart_h
                points.append(QPointF(x, y))

            baseline_y = margin_top + chart_h

            fill_path = QPainterPath()
            fill_path.moveTo(points[0].x(), baseline_y)
            fill_path.lineTo(points[0])
            for i in range(1, len(points)):
                prev = points[i - 1]
                curr = points[i]
                ctrl_x = (prev.x() + curr.x()) / 2
                fill_path.cubicTo(QPointF(ctrl_x, prev.y()), QPointF(ctrl_x, curr.y()), curr)
            fill_path.lineTo(points[-1].x(), baseline_y)
            fill_path.closeSubpath()

            gradient = QLinearGradient(0, margin_top, 0, baseline_y)
            fill_color = QColor(color)
            fill_color.setAlpha(int(80 * self._fill_progress))
            gradient.setColorAt(0, fill_color)
            fill_color2 = QColor(color)
            fill_color2.setAlpha(int(10 * self._fill_progress))
            gradient.setColorAt(1, fill_color2)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawPath(fill_path)

            line_path = QPainterPath()
            line_path.moveTo(points[0])
            for i in range(1, len(points)):
                prev = points[i - 1]
                curr = points[i]
                ctrl_x = (prev.x() + curr.x()) / 2
                line_path.cubicTo(QPointF(ctrl_x, prev.y()), QPointF(ctrl_x, curr.y()), curr)

            pen = QPen(color, 2.5)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(line_path)

        painter.end()
