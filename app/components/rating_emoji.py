from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class RatingEmoji(QWidget):
    ratingChanged = Signal(int)

    def __init__(self, rating=0, parent=None):
        super().__init__(parent)
        self._rating = rating
        self._hover_rating = 0
        self._scale_progress = 1.0
        self._anim = QPropertyAnimation(self, b"scaleProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(5 * 44 + 4, 48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def get_scale_progress(self):
        return self._scale_progress

    def set_scale_progress(self, val):
        self._scale_progress = val
        self.update()

    scaleProgress = Property(float, get_scale_progress, set_scale_progress)

    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        rating = max(0, min(rating, 5))
        if rating != self._rating:
            self._rating = rating
            self._anim.setStartValue(1.0)
            self._anim.setKeyValueAt(0.4, 1.2)
            self._anim.setEndValue(1.0)
            self._anim.start()
            self.ratingChanged.emit(rating)
        self.update()

    def _emoji_at(self, x):
        idx = int((x - 2) / 44)
        return max(1, min(idx + 1, 5))

    def mouseMoveEvent(self, event):
        self._hover_rating = self._emoji_at(event.position().x())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hover_rating = 0
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_rating(self._emoji_at(event.position().x()))
        super().mousePressEvent(event)

    def _draw_face(self, painter, cx, cy, r, level, is_selected):
        is_dark = isDarkTheme()
        if is_selected:
            bg = QColor("#0078D4") if level >= 4 else QColor("#FFB900") if level >= 3 else QColor("#FF4444") if level >= 2 else QColor("#9E9E9E")
        else:
            bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))
        if is_selected:
            painter.setPen(QPen(QColor("#FFFFFF"), 2))
        else:
            painter.setPen(QPen(QColor("#9E9E9E") if is_dark else QColor("#616161"), 1.5))
        eye_y = cy - r * 0.2
        eye_r = r * 0.08
        painter.drawEllipse(QRectF(cx - r * 0.3 - eye_r, eye_y - eye_r, eye_r * 2, eye_r * 2))
        painter.drawEllipse(QRectF(cx + r * 0.3 - eye_r, eye_y - eye_r, eye_r * 2, eye_r * 2))
        mouth_y = cy + r * 0.2
        mouth_w = r * 0.4
        if level == 5:
            painter.drawArc(int(cx - mouth_w), int(mouth_y - r * 0.15), int(mouth_w * 2), int(r * 0.4), 0, -180 * 16)
        elif level == 4:
            painter.drawArc(int(cx - mouth_w), int(mouth_y - r * 0.1), int(mouth_w * 2), int(r * 0.3), 0, -160 * 16)
        elif level == 3:
            painter.drawLine(int(cx - mouth_w), int(mouth_y), int(cx + mouth_w), int(mouth_y))
        elif level == 2:
            painter.drawArc(int(cx - mouth_w), int(mouth_y), int(mouth_w * 2), int(r * 0.3), 0, 180 * 16)
        else:
            painter.drawArc(int(cx - mouth_w), int(mouth_y), int(mouth_w * 2), int(r * 0.35), 0, 180 * 16)
            brow_y = eye_y - r * 0.2
            painter.drawLine(int(cx - r * 0.45), int(brow_y - r * 0.05), int(cx - r * 0.15), int(brow_y + r * 0.05))
            painter.drawLine(int(cx + r * 0.45), int(brow_y - r * 0.05), int(cx + r * 0.15), int(brow_y + r * 0.05))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        display = self._hover_rating if self._hover_rating > 0 else self._rating
        for i in range(5):
            cx = 2 + i * 44 + 22
            cy = 24
            is_selected = (i + 1) <= display
            if is_selected and (i + 1) == display:
                painter.save()
                painter.translate(cx, cy)
                painter.scale(self._scale_progress, self._scale_progress)
                painter.translate(-cx, -cy)
                self._draw_face(painter, cx, cy, 16, i + 1, is_selected)
                painter.restore()
            else:
                self._draw_face(painter, cx, cy, 16, i + 1, is_selected)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
