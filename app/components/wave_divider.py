import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath, QLinearGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class WaveDivider(QWidget):
    def __init__(self, color="#0078D4", parent=None):
        super().__init__(parent)
        self._color = color
        self._phase = 0.0
        self.setFixedHeight(40)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def showEvent(self, event):
        super().showEvent(event)
        self._timer.start(16)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def _tick(self):
        self._phase += 0.06
        self.update()

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        wave_color = QColor(self._color)
        if dark:
            wave_color = wave_color.lighter(120)
        fill_color = QColor(wave_color)
        fill_color.setAlpha(40)
        w = self.width()
        h = self.height()
        mid_y = h / 2
        amplitude = 8
        frequency = 0.03
        path = QPainterPath()
        path.moveTo(0, mid_y)
        for x in range(0, w + 1, 2):
            y = mid_y + amplitude * math.sin(frequency * x + self._phase)
            path.lineTo(x, y)
        path.lineTo(w, h)
        path.lineTo(0, h)
        path.closeSubpath()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(fill_color)
        painter.drawPath(path)
        pen = QPen(wave_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        wave_path = QPainterPath()
        wave_path.moveTo(0, mid_y + amplitude * math.sin(self._phase))
        for x in range(0, w + 1, 2):
            y = mid_y + amplitude * math.sin(frequency * x + self._phase)
            wave_path.lineTo(x, y)
        painter.drawPath(wave_path)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
