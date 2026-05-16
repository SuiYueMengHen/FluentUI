from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QConicalGradient, QPen, QBrush


class ProgressRing(QWidget):
    def __init__(self, size=80, stroke_width=6, parent=None,
                 color1="#0078D4", color2="#60CDFF"):
        super().__init__(parent)
        self._size = size
        self._stroke_width = stroke_width
        self._color1 = color1
        self._color2 = color2
        self._value = 0
        self._indeterminate = False
        self._indet_angle = 0

        self.setFixedSize(size, size)

        self._indet_timer = QTimer(self)
        self._indet_timer.timeout.connect(self._indet_tick)

    def set_value(self, value: int):
        self._value = max(0, min(100, value))
        self._indeterminate = False
        self._indet_timer.stop()
        self.update()

    def set_indeterminate(self, enabled: bool):
        self._indeterminate = enabled
        if enabled:
            self._indet_timer.start(30)
        else:
            self._indet_timer.stop()
        self.update()

    def _indet_tick(self):
        self._indet_angle = (self._indet_angle + 8) % 360
        self.update()

    def _is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            center_x = self.width() / 2
            center_y = self.height() / 2
            radius = (self._size - self._stroke_width) / 2 - 4
            if radius < 1:
                radius = 1

            is_dark = self._is_dark()
            bg_color = QColor("#3D3D3D") if is_dark else QColor("#E5E5E5")
            text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

            bg_pen = QPen(bg_color)
            bg_pen.setWidth(self._stroke_width)
            bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(bg_pen)
            painter.drawArc(
                int(center_x - radius), int(center_y - radius),
                int(radius * 2), int(radius * 2),
                0, 360 * 16
            )

            if self._indeterminate:
                gradient = QConicalGradient(center_x, center_y, self._indet_angle)
                gradient.setColorAt(0, QColor(self._color1))
                gradient.setColorAt(0.7, QColor(self._color2))
                gradient.setColorAt(1, QColor(0, 0, 0, 0))

                pen = QPen(QBrush(gradient), self._stroke_width)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)
                span = 90 * 16
                painter.drawArc(
                    int(center_x - radius), int(center_y - radius),
                    int(radius * 2), int(radius * 2),
                    self._indet_angle * 16, span
                )
            else:
                span_angle = int(-self._value / 100 * 360 * 16)
                start_angle = 90 * 16

                gradient = QConicalGradient(center_x, center_y, 90)
                gradient.setColorAt(0, QColor(self._color1))
                gradient.setColorAt(1, QColor(self._color2))

                pen = QPen(QBrush(gradient), self._stroke_width)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)
                painter.drawArc(
                    int(center_x - radius), int(center_y - radius),
                    int(radius * 2), int(radius * 2),
                    start_angle, span_angle
                )

                painter.setPen(text_color)
                painter.setFont(self.font())
                painter.drawText(
                    QRectF(center_x - radius, center_y - radius, radius * 2, radius * 2),
                    Qt.AlignmentFlag.AlignCenter,
                    f"{self._value}%"
                )
        finally:
            if painter.isActive():
                painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self._indeterminate:
            self._indet_timer.start(30)

    def hideEvent(self, event):
        if self._indet_timer.isActive():
            self._indet_timer.stop()
        super().hideEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
