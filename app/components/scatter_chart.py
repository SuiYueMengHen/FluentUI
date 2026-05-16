from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import isDarkTheme


class ScatterChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._pop_progress = 0.0
        self.setMinimumSize(200, 150)

        self._anim = QPropertyAnimation(self, b"_pop_progress_prop")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_pop_progress(self):
        return self._pop_progress

    def set_pop_progress(self, val):
        self._pop_progress = val
        self.update()

    _pop_progress_prop = Property(float, get_pop_progress, set_pop_progress)

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
        margin_top = 20
        margin_bottom = 40

        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if not self._data or chart_w <= 0 or chart_h <= 0:
            painter.end()
            return

        x_vals = [d["x"] for d in self._data]
        y_vals = [d["y"] for d in self._data]
        min_x = min(x_vals)
        max_x = max(x_vals)
        min_y = min(y_vals)
        max_y = max(y_vals)
        x_range = max_x - min_x if max_x != min_x else 1
        y_range = max_y - min_y if max_y != min_y else 1

        grid_pen = QPen(grid_color, 1, Qt.PenStyle.DashLine)
        painter.setPen(grid_pen)
        grid_count = 5
        for i in range(grid_count + 1):
            y = margin_top + chart_h - (i / grid_count) * chart_h
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))
        for i in range(grid_count + 1):
            x = margin_left + (i / grid_count) * chart_w
            painter.drawLine(int(x), int(margin_top), int(x), int(margin_top + chart_h))

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
            val = min_y + y_range * i / grid_count
            painter.drawText(QRectF(0, y - 10, margin_left - 5, 20), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{val:.1f}")
        for i in range(grid_count + 1):
            x = margin_left + (i / grid_count) * chart_w
            val = min_x + x_range * i / grid_count
            painter.drawText(QRectF(x - 25, margin_top + chart_h + 5, 50, 20), Qt.AlignmentFlag.AlignCenter, f"{val:.1f}")

        cx = margin_left + chart_w / 2
        cy = margin_top + chart_h / 2

        for d in self._data:
            px = margin_left + ((d["x"] - min_x) / x_range) * chart_w
            py = margin_top + chart_h - ((d["y"] - min_y) / y_range) * chart_h

            anim_x = cx + (px - cx) * self._pop_progress
            anim_y = cy + (py - cy) * self._pop_progress

            color = QColor(d.get("color", "#0078D4"))
            size = d.get("size", 8) * self._pop_progress

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(anim_x, anim_y), size / 2, size / 2)

            border_color = QColor(color)
            border_color.setAlpha(60)
            painter.setBrush(QBrush(border_color))
            painter.drawEllipse(QPointF(anim_x, anim_y), size / 2 + 3, size / 2 + 3)

        painter.end()
