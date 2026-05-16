from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class BarChart(QWidget):
    def __init__(self, data=None, labels=None, colors=None, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._labels = labels or []
        self._colors = colors or []
        self._anim_progress = 0.0
        self.setMinimumSize(200, 150)

        self._anim = QPropertyAnimation(self, b"_anim_progress_prop")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_anim_progress(self):
        return self._anim_progress

    def set_anim_progress(self, val):
        self._anim_progress = val
        self.update()

    _anim_progress_prop = Property(float, get_anim_progress, set_anim_progress)

    def _is_dark(self):
        return isDarkTheme()

    def set_data(self, data, labels=None):
        self._data = data
        if labels is not None:
            self._labels = labels
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def refresh_theme(self):
        self.update()
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        grid_color = QColor("#404040") if is_dark else QColor("#E0E0E0")
        axis_text_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
        value_text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

        w = self.width()
        h = self.height()
        margin_left = 50
        margin_right = 20
        margin_top = 30
        margin_bottom = 40

        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if not self._data or chart_w <= 0 or chart_h <= 0:
            painter.end()
            return

        max_val = max(self._data) if self._data else 1
        if max_val == 0:
            max_val = 1

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
            val = max_val * i / grid_count
            painter.drawText(QRectF(0, y - 10, margin_left - 5, 20), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"{val:.0f}")

        bar_count = len(self._data)
        if bar_count == 0:
            painter.end()
            return
        bar_spacing = chart_w / bar_count
        bar_width = bar_spacing * 0.6

        default_colors = ["#0078D4", "#00B4D8", "#6CCB5F", "#FFB900", "#FF6B6B", "#B4A0FF"]
        for i, val in enumerate(self._data):
            if i < len(self._colors):
                color = QColor(self._colors[i])
            else:
                color = QColor(default_colors[i % len(default_colors)])

            bar_h = (val / max_val) * chart_h * self._anim_progress
            x = margin_left + i * bar_spacing + (bar_spacing - bar_width) / 2
            y = margin_top + chart_h - bar_h

            path = QPainterPath()
            radius = min(4, bar_width / 2)
            rect = QRectF(x, y, bar_width, bar_h)
            if bar_h > radius * 2:
                path.moveTo(x, y + bar_h)
                path.lineTo(x, y + radius)
                path.arcTo(QRectF(x, y, radius * 2, radius * 2), 180, -90)
                path.lineTo(x + bar_width - radius, y)
                path.arcTo(QRectF(x + bar_width - radius * 2, y, radius * 2, radius * 2), 90, -90)
                path.lineTo(x + bar_width, y + bar_h)
                path.closeSubpath()
            else:
                path.addRect(rect)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawPath(path)

            if self._anim_progress > 0.8:
                painter.setPen(value_text_color)
                font.setPixelSize(11)
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(QRectF(x - 5, y - 20, bar_width + 10, 18), Qt.AlignmentFlag.AlignCenter, f"{val:.0f}")

            if i < len(self._labels):
                painter.setPen(axis_text_color)
                font.setBold(False)
                font.setPixelSize(11)
                painter.setFont(font)
                painter.drawText(QRectF(x - 5, margin_top + chart_h + 5, bar_width + 10, 30), Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextWordWrap, self._labels[i])

        painter.end()
