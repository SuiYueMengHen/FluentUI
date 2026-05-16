import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class RatingStars(QWidget):
    ratingChanged = Signal(int)

    def __init__(self, rating=0, max_stars=5, parent=None):
        super().__init__(parent)
        self._rating = rating
        self._max_stars = max_stars
        self._hover_rating = 0
        self._fill_progress = 0.0
        self._anim = QPropertyAnimation(self, b"fillProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(max_stars * 28 + 4, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def get_fill_progress(self):
        return self._fill_progress

    def set_fill_progress(self, val):
        self._fill_progress = val
        self.update()

    fillProgress = Property(float, get_fill_progress, set_fill_progress)

    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        rating = max(0, min(rating, self._max_stars))
        if rating != self._rating:
            self._rating = rating
            self._fill_progress = 0.0
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(1.0)
            self._anim.start()
            self.ratingChanged.emit(rating)
        self.update()

    def _star_at(self, x):
        star_idx = int((x - 2) / 28)
        return max(1, min(star_idx + 1, self._max_stars))

    def mouseMoveEvent(self, event):
        self._hover_rating = self._star_at(event.position().x())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hover_rating = 0
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_rating(self._star_at(event.position().x()))
        super().mousePressEvent(event)

    def _create_star_path(self, cx, cy, outer_r, inner_r):
        path = QPainterPath()
        for i in range(5):
            outer_angle = math.radians(-90 + i * 72)
            inner_angle = math.radians(-90 + i * 72 + 36)
            ox = cx + outer_r * math.cos(outer_angle)
            oy = cy + outer_r * math.sin(outer_angle)
            ix = cx + inner_r * math.cos(inner_angle)
            iy = cy + inner_r * math.sin(inner_angle)
            if i == 0:
                path.moveTo(ox, oy)
            else:
                path.lineTo(ox, oy)
            path.lineTo(ix, iy)
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        filled_color = QColor("#FFB900")
        empty_color = QColor("#505050") if is_dark else QColor("#E0E0E0")
        display_rating = self._hover_rating if self._hover_rating > 0 else self._rating
        for i in range(self._max_stars):
            cx = 2 + i * 28 + 14
            cy = 14
            star_path = self._create_star_path(cx, cy, 11, 5)
            star_num = i + 1
            if star_num <= display_rating:
                fill = self._fill_progress if star_num > self._rating - 1 else 1.0
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(filled_color)
                painter.drawPath(star_path)
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(empty_color)
                painter.drawPath(star_path)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
