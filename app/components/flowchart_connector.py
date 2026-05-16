from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class FlowchartConnector(QWidget):
    def __init__(self, direction="down", label="", parent=None):
        super().__init__(parent)
        self._direction = direction
        self._label = label
        self._draw_progress = 0.0

        if direction in ("up", "down"):
            self.setFixedSize(40, 48)
        else:
            self.setFixedSize(48, 40)

        self._anim = QPropertyAnimation(self, b"drawProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_draw_progress(self):
        return self._draw_progress

    def set_draw_progress(self, val):
        self._draw_progress = val
        self.update()

    drawProgress = Property(float, get_draw_progress, set_draw_progress)

    def animate_in(self):
        self._draw_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def refresh_theme(self):
        self.update()

    def _is_dark(self):
        return isDarkTheme()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self._is_dark()
        line_color = QColor("#AAAAAA") if dark else QColor("#666666")
        label_color = QColor("#CCCCCC") if dark else QColor("#555555")

        progress = self._draw_progress
        w = self.width()
        h = self.height()

        if self._direction == "down":
            self._draw_arrow(painter, line_color, w / 2, 0, w / 2, h * progress, "down")
        elif self._direction == "up":
            self._draw_arrow(painter, line_color, w / 2, h, w / 2, h * (1 - progress), "up")
        elif self._direction == "right":
            self._draw_arrow(painter, line_color, 0, h / 2, w * progress, h / 2, "right")
        elif self._direction == "left":
            self._draw_arrow(painter, line_color, w, h / 2, w * (1 - progress), h / 2, "left")

        if self._label and progress > 0.5:
            font = QFont()
            font.setPointSize(8)
            painter.setFont(font)
            painter.setPen(label_color)
            label_rect = QRectF(0, 0, w, h)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, self._label)

        painter.end()

    def _draw_arrow(self, painter, color, x1, y1, x2, y2, direction):
        pen = QPen(color)
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        path = QPainterPath()
        path.moveTo(x1, y1)
        path.lineTo(x2, y2)
        painter.drawPath(path)

        arrow_size = 8
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)

        if direction == "down":
            triangle = QPainterPath()
            triangle.moveTo(x2, y2)
            triangle.lineTo(x2 - arrow_size / 2, y2 - arrow_size)
            triangle.lineTo(x2 + arrow_size / 2, y2 - arrow_size)
            triangle.closeSubpath()
            painter.drawPath(triangle)
        elif direction == "up":
            triangle = QPainterPath()
            triangle.moveTo(x2, y2)
            triangle.lineTo(x2 - arrow_size / 2, y2 + arrow_size)
            triangle.lineTo(x2 + arrow_size / 2, y2 + arrow_size)
            triangle.closeSubpath()
            painter.drawPath(triangle)
        elif direction == "right":
            triangle = QPainterPath()
            triangle.moveTo(x2, y2)
            triangle.lineTo(x2 - arrow_size, y2 - arrow_size / 2)
            triangle.lineTo(x2 - arrow_size, y2 + arrow_size / 2)
            triangle.closeSubpath()
            painter.drawPath(triangle)
        elif direction == "left":
            triangle = QPainterPath()
            triangle.moveTo(x2, y2)
            triangle.lineTo(x2 + arrow_size, y2 - arrow_size / 2)
            triangle.lineTo(x2 + arrow_size, y2 + arrow_size / 2)
            triangle.closeSubpath()
            painter.drawPath(triangle)

    def showEvent(self, event):
        super().showEvent(event)
        self.animate_in()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()
        super().hideEvent(event)
