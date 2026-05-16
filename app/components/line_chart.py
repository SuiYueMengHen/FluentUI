from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class LineChart(QWidget):
    def __init__(self, series=None, labels=None, parent=None):
        super().__init__(parent)
        self._series = series or []
        self._labels = labels or []
        self._draw_progress = 0.0
        self.setMinimumSize(200, 150)

        self._anim = QPropertyAnimation(self, b"_draw_progress_prop")
        self._anim.setDuration(400)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_draw_progress(self):
        return self._draw_progress

    def set_draw_progress(self, val):
        self._draw_progress = val
        self.update()

    _draw_progress_prop = Property(float, get_draw_progress, set_draw_progress)

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
        min_val = min(all_vals)
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

        max_points = max(len(s.get("data", [])) for s in self._series)
        if max_points == 0:
            painter.end()
            return

        if self._labels:
            step = chart_w / (len(self._labels) - 1) if len(self._labels) > 1 else chart_w
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

            visible_count = max(2, int(len(points) * self._draw_progress))
            visible_points = points[:visible_count]

            if len(visible_points) >= 2:
                path = QPainterPath()
                path.moveTo(visible_points[0])
                for i in range(1, len(visible_points)):
                    prev = visible_points[i - 1]
                    curr = visible_points[i]
                    ctrl_x = (prev.x() + curr.x()) / 2
                    path.cubicTo(QPointF(ctrl_x, prev.y()), QPointF(ctrl_x, curr.y()), curr)

                pen = QPen(color, 2.5)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawPath(path)

                for pt in visible_points:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(QBrush(color))
                    painter.drawEllipse(pt, 4, 4)
                    painter.setBrush(QBrush(QColor("#FFFFFF") if not is_dark else QColor("#2D2D2D")))
                    painter.drawEllipse(pt, 2, 2)

        legend_y = 8
        legend_x = margin_left
        font.setPixelSize(11)
        painter.setFont(font)
        for s in self._series:
            color = QColor(s.get("color", "#0078D4"))
            name = s.get("name", "")
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, 12, 12), 2, 2)
            painter.setPen(axis_text_color)
            painter.drawText(QRectF(legend_x + 16, legend_y - 2, 100, 16), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, name)
            legend_x += 120

        painter.end()
