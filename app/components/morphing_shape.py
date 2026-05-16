import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class MorphingShape(QWidget):
    def __init__(self, color="#0078D4", parent=None):
        super().__init__(parent)
        self._color = color
        self._current_shape = "circle"
        self._target_shape = "circle"
        self._morph_progress = 1.0
        self.setFixedSize(120, 120)
        self._anim = QPropertyAnimation(self, b"morphProgress")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_morph_progress(self):
        return self._morph_progress

    def set_morph_progress(self, val):
        self._morph_progress = val
        self.update()

    morphProgress = Property(float, get_morph_progress, set_morph_progress)

    def morph_to(self, shape_name):
        if shape_name not in ("circle", "square", "triangle", "star"):
            return
        self._current_shape = self._target_shape
        self._target_shape = shape_name
        self._morph_progress = 0.0
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def _shape_points(self, shape, cx, cy, r):
        if shape == "circle":
            pts = []
            for i in range(36):
                angle = 2 * math.pi * i / 36
                pts.append(QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle)))
            return pts
        elif shape == "square":
            s = r * 0.85
            return [QPointF(cx - s, cy - s), QPointF(cx + s, cy - s), QPointF(cx + s, cy + s), QPointF(cx - s, cy + s)]
        elif shape == "triangle":
            pts = []
            for i in range(3):
                angle = -math.pi / 2 + 2 * math.pi * i / 3
                pts.append(QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle)))
            return pts
        elif shape == "star":
            pts = []
            for i in range(10):
                angle = -math.pi / 2 + 2 * math.pi * i / 10
                rad = r if i % 2 == 0 else r * 0.45
                pts.append(QPointF(cx + rad * math.cos(angle), cy + rad * math.sin(angle)))
            return pts
        return []

    def _interpolate_points(self, pts1, pts2, t):
        max_len = max(len(pts1), len(pts2))
        while len(pts1) < max_len:
            pts1.append(pts1[-1])
        while len(pts2) < max_len:
            pts2.append(pts2[-1])
        result = []
        for p1, p2 in zip(pts1, pts2):
            x = p1.x() + (p2.x() - p1.x()) * t
            y = p1.y() + (p2.y() - p1.y()) * t
            result.append(QPointF(x, y))
        return result

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        color = QColor(self._color)
        if dark:
            color = color.lighter(120)
        cx = self.width() / 2
        cy = self.height() / 2
        r = min(self.width(), self.height()) / 2 - 10
        pts1 = self._shape_points(self._current_shape, cx, cy, r)
        pts2 = self._shape_points(self._target_shape, cx, cy, r)
        t = self._morph_progress
        points = self._interpolate_points(pts1, pts2, t)
        if points:
            path = QPainterPath()
            path.moveTo(points[0])
            for p in points[1:]:
                path.lineTo(p)
            path.closeSubpath()
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
