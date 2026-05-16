from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QConicalGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class CircularProgress(QWidget):
    def __init__(self, value=0, size=100, stroke_width=8, color="#0078D4", parent=None):
        super().__init__(parent)
        self._value = value
        self._size = size
        self._stroke_width = stroke_width
        self._color = color
        self._arc_progress = 0.0
        self.setFixedSize(size, size)
        self._anim = QPropertyAnimation(self, b"arcProgress")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_arc_progress(self):
        return self._arc_progress

    def set_arc_progress(self, val):
        self._arc_progress = val
        self.update()

    arcProgress = Property(float, get_arc_progress, set_arc_progress)

    def set_value(self, value):
        self._value = max(0, min(100, value))
        self._anim.stop()
        self._arc_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            dark = isDarkTheme()
            bg_arc = QColor("#404040") if dark else QColor("#E5E5E5")
            text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
            cx = self.width() / 2
            cy = self.height() / 2
            radius = (self._size - self._stroke_width) / 2 - 2
            pen = QPen(bg_arc, self._stroke_width)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawArc(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2), 0, 360 * 16)
            span = int(-self._value / 100 * 360 * self._arc_progress * 16)
            gradient = QConicalGradient(cx, cy, 90)
            gradient.setColorAt(0, QColor(self._color))
            gradient.setColorAt(1, QColor(self._color).lighter(130))
            pen = QPen(QBrush(gradient), self._stroke_width)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawArc(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2), 90 * 16, span)
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(int(self._size / 5))
            font.setBold(True)
            painter.setFont(font)
            display_val = int(self._value * self._arc_progress)
            painter.drawText(QRectF(cx - radius, cy - radius, radius * 2, radius * 2), Qt.AlignmentFlag.AlignCenter, f"{display_val}%")
        finally:
            painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
