from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class LikeButton(QWidget):
    likedChanged = Signal(bool, int)

    def __init__(self, count=0, liked=False, parent=None):
        super().__init__(parent)
        self._liked = liked
        self._count = count
        self._bounce_scale = 1.0
        self.setFixedSize(80, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._anim = QPropertyAnimation(self, b"bounceScale")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_bounce_scale(self):
        return self._bounce_scale

    def set_bounce_scale(self, val):
        self._bounce_scale = val
        self.update()

    bounceScale = Property(float, get_bounce_scale, set_bounce_scale)

    def is_liked(self):
        return self._liked

    def set_liked(self, liked, animate=True):
        self._liked = liked
        if animate:
            self._anim.setStartValue(1.0)
            self._anim.setKeyValueAt(0.4, 1.3)
            self._anim.setEndValue(1.0)
            self._anim.start()
        self.update()

    def get_count(self):
        return self._count

    def set_count(self, count):
        self._count = count
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._liked = not self._liked
            if self._liked:
                self._count += 1
            else:
                self._count = max(0, self._count - 1)
            self.set_liked(self._liked)
            self.likedChanged.emit(self._liked, self._count)
        super().mousePressEvent(event)

    def _create_heart_path(self, cx, cy, size):
        path = QPainterPath()
        s = size / 2
        path.moveTo(cx, cy + s * 0.3)
        path.cubicTo(cx, cy - s * 0.3, cx - s, cy - s * 0.3, cx - s, cy + s * 0.1)
        path.cubicTo(cx - s, cy + s * 0.6, cx, cy + s * 0.9, cx, cy + s)
        path.cubicTo(cx, cy + s * 0.9, cx + s, cy + s * 0.6, cx + s, cy + s * 0.1)
        path.cubicTo(cx + s, cy - s * 0.3, cx, cy - s * 0.3, cx, cy + s * 0.3)
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        painter.save()
        center_x = 20
        center_y = self.height() / 2
        painter.translate(center_x, center_y)
        painter.scale(self._bounce_scale, self._bounce_scale)
        painter.translate(-center_x, -center_y)
        heart_size = 14
        heart_path = self._create_heart_path(center_x, center_y - 1, heart_size)
        if self._liked:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#FF4444"))
            painter.drawPath(heart_path)
        else:
            outline_color = QColor("#616161") if is_dark else QColor("#9E9E9E")
            painter.setPen(QPen(outline_color, 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(heart_path)
        painter.restore()
        text_color = QColor("#D4D4D4") if is_dark else QColor("#1A1A1A")
        painter.setPen(text_color)
        font = QFont()
        font.setPixelSize(13)
        painter.setFont(font)
        text_rect = QRectF(36, 0, self.width() - 36, self.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, str(self._count))
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
