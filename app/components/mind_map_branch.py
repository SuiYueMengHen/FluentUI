from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath
from qfluentwidgets import isDarkTheme


class MindMapBranch(QWidget):
    def __init__(self, direction="right", parent=None):
        super().__init__(parent)
        self._direction = direction
        self._draw_progress = 0.0

        if direction in ("up", "down"):
            self.setFixedSize(24, 40)
        else:
            self.setFixedSize(40, 24)

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
        w = self.width()
        h = self.height()
        progress = self._draw_progress

        if self._direction == "right":
            gradient = QLinearGradient(0, 0, w, 0)
            start, end = QPointF(0, h / 2), QPointF(w * progress, h / 2)
            ctrl1 = QPointF(w * progress * 0.4, h / 2)
            ctrl2 = QPointF(w * progress * 0.6, h / 2)
        elif self._direction == "left":
            gradient = QLinearGradient(w, 0, 0, 0)
            start, end = QPointF(w, h / 2), QPointF(w * (1 - progress), h / 2)
            ctrl1 = QPointF(w * (1 - progress * 0.4), h / 2)
            ctrl2 = QPointF(w * (1 - progress * 0.6), h / 2)
        elif self._direction == "down":
            gradient = QLinearGradient(0, 0, 0, h)
            start, end = QPointF(w / 2, 0), QPointF(w / 2, h * progress)
            ctrl1 = QPointF(w / 2, h * progress * 0.4)
            ctrl2 = QPointF(w / 2, h * progress * 0.6)
        else:
            gradient = QLinearGradient(0, h, 0, 0)
            start, end = QPointF(w / 2, h), QPointF(w / 2, h * (1 - progress))
            ctrl1 = QPointF(w / 2, h * (1 - progress * 0.4))
            ctrl2 = QPointF(w / 2, h * (1 - progress * 0.6))

        if dark:
            gradient.setColorAt(0, QColor("#0078D4"))
            gradient.setColorAt(1, QColor("#60CDFF"))
        else:
            gradient.setColorAt(0, QColor("#0078D4"))
            gradient.setColorAt(1, QColor("#005A9E"))

        pen = QPen(QBrush(gradient), 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        path = QPainterPath()
        path.moveTo(start)
        path.cubicTo(ctrl1, ctrl2, end)
        painter.drawPath(path)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        self.animate_in()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()
        super().hideEvent(event)
