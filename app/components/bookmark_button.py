from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class BookmarkButton(QWidget):
    bookmarkedChanged = Signal(bool)

    def __init__(self, bookmarked=False, parent=None):
        super().__init__(parent)
        self._bookmarked = bookmarked
        self._flip_progress = 0.0
        self._hover = False
        self._anim = QPropertyAnimation(self, b"flipProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(36, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def get_flip_progress(self):
        return self._flip_progress

    def set_flip_progress(self, val):
        self._flip_progress = val
        self.update()

    flipProgress = Property(float, get_flip_progress, set_flip_progress)

    def is_bookmarked(self):
        return self._bookmarked

    def set_bookmarked(self, bookmarked):
        if bookmarked != self._bookmarked:
            self._bookmarked = bookmarked
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(1.0)
            self._anim.start()
            self.bookmarkedChanged.emit(bookmarked)
        self.update()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_bookmarked(not self._bookmarked)
        super().mousePressEvent(event)

    def _create_bookmark_path(self, x, y, w, h):
        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x + w, y)
        path.lineTo(x + w, y + h * 0.85)
        path.lineTo(x + w / 2, y + h * 0.65)
        path.lineTo(x, y + h * 0.85)
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        painter.save()
        cx = self.width() / 2
        cy = self.height() / 2
        scale_x = abs(1.0 - 2.0 * self._flip_progress) if self._flip_progress <= 0.5 else abs(-1.0 + 2.0 * self._flip_progress)
        if scale_x < 0.05:
            scale_x = 0.05
        painter.translate(cx, cy)
        painter.scale(scale_x, 1.0)
        painter.translate(-cx, -cy)
        bm_w = 16
        bm_h = 22
        bm_x = (self.width() - bm_w) / 2
        bm_y = (self.height() - bm_h) / 2
        show_bookmarked = self._bookmarked
        if self._flip_progress > 0 and self._flip_progress < 0.5:
            show_bookmarked = not self._bookmarked
        elif self._flip_progress >= 0.5:
            show_bookmarked = self._bookmarked
        bookmark_path = self._create_bookmark_path(bm_x, bm_y, bm_w, bm_h)
        if show_bookmarked:
            painter.setPen(Qt.PenStyle.NoPen)
            fill_color = QColor("#FFB900")
            if self._hover:
                fill_color = fill_color.darker(110)
            painter.setBrush(fill_color)
            painter.drawPath(bookmark_path)
        else:
            outline_color = QColor("#616161") if is_dark else QColor("#9E9E9E")
            if self._hover:
                outline_color = QColor("#FFB900")
            painter.setPen(QPen(outline_color, 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(bookmark_path)
        painter.restore()
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
