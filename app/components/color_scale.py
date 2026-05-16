from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient
from qfluentwidgets import isDarkTheme


class ColorScale(QWidget):
    def __init__(self, color_low="#E8F5E9", color_high="#1B5E20", min_val=0, max_val=100, parent=None):
        super().__init__(parent)
        self._color_low = color_low
        self._color_high = color_high
        self._min_val = min_val
        self._max_val = max_val
        self._progress = 0.0
        self._anim = QPropertyAnimation(self, b"scaleProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedHeight(44)
        self.setMinimumWidth(200)

    def _is_dark(self):
        return isDarkTheme()

    def get_progress(self):
        return self._progress

    def set_progress(self, val):
        self._progress = val
        self.update()

    scaleProgress = Property(float, get_progress, set_progress)

    def set_range(self, min_val, max_val):
        self._min_val = min_val
        self._max_val = max_val
        self.update()

    def set_colors(self, color_low, color_high):
        self._color_low = color_low
        self._color_high = color_high
        self.update()

    def show_animated(self):
        self._progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        label_color = QColor("#616161") if not is_dark else QColor("#9E9E9E")
        border_color = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")

        bar_margin = 32
        bar_h = 14
        bar_y = (self.height() - bar_h) / 2
        bar_w = (self.width() - bar_margin * 2) * self._progress

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        bg_rect = QRectF(bar_margin, bar_y, self.width() - bar_margin * 2, bar_h)
        painter.drawRoundedRect(bg_rect, 7, 7)

        if bar_w > 0:
            gradient = QLinearGradient(bar_margin, 0, bar_margin + bar_w, 0)
            gradient.setColorAt(0.0, QColor(self._color_low))
            gradient.setColorAt(1.0, QColor(self._color_high))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            painter.setClipRect(QRectF(bar_margin, bar_y, bar_w, bar_h))
            painter.drawRoundedRect(bg_rect, 7, 7)
            painter.setClipping(False)

        tick_count = 5
        tick_spacing = (self.width() - bar_margin * 2) / max(tick_count - 1, 1)
        painter.setPen(QPen(border_color, 1))
        for i in range(tick_count):
            tx = bar_margin + tick_spacing * i
            painter.drawLine(int(tx), int(bar_y + bar_h), int(tx), int(bar_y + bar_h + 4))

        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(label_color)

        min_text = str(self._min_val)
        max_text = str(self._max_val)
        min_rect = QRectF(0, bar_y + bar_h + 4, bar_margin * 2, 16)
        max_rect = QRectF(self.width() - bar_margin * 2, bar_y + bar_h + 4, bar_margin * 2, 16)
        painter.drawText(min_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, min_text)
        painter.drawText(max_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, max_text)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
