from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import isDarkTheme


class HeatmapChart(QWidget):
    def __init__(self, data=None, x_labels=None, y_labels=None, color_low="#E8F5E9", color_high="#1B5E20", parent=None):
        super().__init__(parent)
        self._data = data or []
        self._x_labels = x_labels or []
        self._y_labels = y_labels or []
        self._color_low = color_low
        self._color_high = color_high
        self._fade_progress = 0.0
        self.setMinimumSize(200, 150)

        self._anim = QPropertyAnimation(self, b"_fade_progress_prop")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_fade_progress(self):
        return self._fade_progress

    def set_fade_progress(self, val):
        self._fade_progress = val
        self.update()

    _fade_progress_prop = Property(float, get_fade_progress, set_fade_progress)

    def _is_dark(self):
        return isDarkTheme()

    def refresh_theme(self):
        self.update()
        self.repaint()

    def _interpolate_color(self, ratio):
        low = QColor(self._color_low)
        high = QColor(self._color_high)
        r = int(low.red() + (high.red() - low.red()) * ratio)
        g = int(low.green() + (high.green() - low.green()) * ratio)
        b = int(low.blue() + (high.blue() - low.blue()) * ratio)
        return QColor(r, g, b)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        label_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
        value_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

        w = self.width()
        h = self.height()

        if not self._data or not self._data[0]:
            painter.end()
            return

        rows = len(self._data)
        cols = len(self._data[0])

        margin_left = 60
        margin_right = 20
        margin_top = 20
        margin_bottom = 40

        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if chart_w <= 0 or chart_h <= 0:
            painter.end()
            return

        cell_w = chart_w / cols
        cell_h = chart_h / rows

        all_vals = []
        for row in self._data:
            for v in row:
                all_vals.append(v)
        min_val = min(all_vals)
        max_val = max(all_vals)
        val_range = max_val - min_val if max_val != min_val else 1

        font = QFont()
        font.setPixelSize(11)
        painter.setFont(font)

        for r in range(rows):
            row_fade = max(0.0, min(1.0, self._fade_progress * rows - r))
            if row_fade <= 0:
                continue

            for c in range(cols):
                val = self._data[r][c]
                ratio = (val - min_val) / val_range
                color = self._interpolate_color(ratio)
                color.setAlpha(int(255 * row_fade))

                x = margin_left + c * cell_w
                y = margin_top + r * cell_h
                rect = QRectF(x + 1, y + 1, cell_w - 2, cell_h - 2)

                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRoundedRect(rect, 3, 3)

                if row_fade > 0.7 and cell_w > 30 and cell_h > 20:
                    brightness = color.red() * 0.299 + color.green() * 0.587 + color.blue() * 0.114
                    text_c = QColor("#FFFFFF") if brightness < 128 else QColor("#1A1A1A")
                    painter.setPen(text_c)
                    font.setPixelSize(min(11, int(cell_h * 0.4)))
                    painter.setFont(font)
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{val:.1f}")

        painter.setPen(label_color)
        font.setPixelSize(11)
        painter.setFont(font)

        for c in range(cols):
            if c < len(self._x_labels):
                x = margin_left + c * cell_w + cell_w / 2
                painter.drawText(QRectF(x - cell_w / 2, margin_top + chart_h + 5, cell_w, 30), Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self._x_labels[c])

        for r in range(rows):
            if r < len(self._y_labels):
                y = margin_top + r * cell_h + cell_h / 2
                painter.drawText(QRectF(0, y - 10, margin_left - 5, 20), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._y_labels[r])

        painter.end()
