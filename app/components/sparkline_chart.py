from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath
from qfluentwidgets import isDarkTheme


class SparklineChart(QWidget):
    def __init__(self, data=None, color="#0078D4", parent=None):
        super().__init__(parent)
        self._data = data or []
        self._color = color
        self._draw_progress = 0.0
        self.setFixedHeight(32)
        self.setMinimumWidth(60)

        self._anim = QPropertyAnimation(self, b"_draw_progress_prop")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._first_show = True

    def get_draw_progress(self):
        return self._draw_progress

    def set_draw_progress(self, val):
        self._draw_progress = val
        self.update()

    _draw_progress_prop = Property(float, get_draw_progress, set_draw_progress)

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self._anim.start()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.pause()
        super().hideEvent(event)

    def _is_dark(self):
        return isDarkTheme()

    def refresh_theme(self):
        self.update()
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        color = QColor(self._color)

        w = self.width()
        h = self.height()
        padding_x = 4
        padding_y = 4

        chart_w = w - padding_x * 2
        chart_h = h - padding_y * 2

        if len(self._data) < 2 or chart_w <= 0 or chart_h <= 0:
            painter.end()
            return

        max_val = max(self._data)
        min_val = min(self._data)
        val_range = max_val - min_val if max_val != min_val else 1

        step = chart_w / (len(self._data) - 1)
        points = []
        for i, val in enumerate(self._data):
            x = padding_x + i * step
            y = padding_y + chart_h - ((val - min_val) / val_range) * chart_h
            points.append(QPointF(x, y))

        visible_count = max(2, int(len(points) * self._draw_progress))
        visible_points = points[:visible_count]

        if len(visible_points) >= 2:
            fill_path = QPainterPath()
            fill_path.moveTo(visible_points[0].x(), h - padding_y)
            fill_path.lineTo(visible_points[0])
            for i in range(1, len(visible_points)):
                prev = visible_points[i - 1]
                curr = visible_points[i]
                ctrl_x = (prev.x() + curr.x()) / 2
                fill_path.cubicTo(QPointF(ctrl_x, prev.y()), QPointF(ctrl_x, curr.y()), curr)
            fill_path.lineTo(visible_points[-1].x(), h - padding_y)
            fill_path.closeSubpath()

            gradient = QLinearGradient(0, 0, 0, h)
            fill_color = QColor(color)
            fill_color.setAlpha(40)
            gradient.setColorAt(0, fill_color)
            fill_color2 = QColor(color)
            fill_color2.setAlpha(5)
            gradient.setColorAt(1, fill_color2)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawPath(fill_path)

            line_path = QPainterPath()
            line_path.moveTo(visible_points[0])
            for i in range(1, len(visible_points)):
                prev = visible_points[i - 1]
                curr = visible_points[i]
                ctrl_x = (prev.x() + curr.x()) / 2
                line_path.cubicTo(QPointF(ctrl_x, prev.y()), QPointF(ctrl_x, curr.y()), curr)

            pen = QPen(color, 1.5)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(line_path)

            last = visible_points[-1]
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(last, 2.5, 2.5)

        painter.end()
