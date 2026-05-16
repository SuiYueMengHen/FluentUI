from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class CarouselWidget(QWidget):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._items = []
        if items:
            for item in items:
                if isinstance(item, str):
                    self._items.append({"title": item, "color": "#0078D4"})
                else:
                    self._items.append(item)
        self._current_index = 0
        self._slide_offset = 0.0
        self._hovered_arrow = 0
        self.setMinimumSize(400, 200)
        self.setMouseTracking(True)

        self._slide_anim = QPropertyAnimation(self, b"slideOffset")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_slide_offset(self):
        return self._slide_offset

    def set_slide_offset(self, val):
        self._slide_offset = val
        self.update()

    slideOffset = Property(float, get_slide_offset, set_slide_offset)

    def _is_dark(self):
        return isDarkTheme()

    def _prev(self):
        if not self._items:
            return
        self._slide_anim.setStartValue(-1.0)
        self._slide_anim.setEndValue(0.0)
        self._current_index = (self._current_index - 1) % len(self._items)
        self._slide_offset = -1.0
        self._slide_anim.start()

    def _next(self):
        if not self._items:
            return
        self._slide_anim.setStartValue(1.0)
        self._slide_anim.setEndValue(0.0)
        self._current_index = (self._current_index + 1) % len(self._items)
        self._slide_offset = 1.0
        self._slide_anim.start()

    def _left_arrow_rect(self):
        return QRectF(8, self.height() / 2 - 16, 32, 32)

    def _right_arrow_rect(self):
        return QRectF(self.width() - 40, self.height() / 2 - 16, 32, 32)

    def _dot_rects(self):
        rects = []
        n = len(self._items)
        if n == 0:
            return rects
        dot_r = 5
        total_w = n * dot_r * 2 + (n - 1) * 8
        start_x = (self.width() - total_w) / 2
        y = self.height() - 20
        for i in range(n):
            x = start_x + i * (dot_r * 2 + 8) + dot_r
            rects.append(QRectF(x - dot_r, y - dot_r, dot_r * 2, dot_r * 2))
        return rects

    def mousePressEvent(self, event):
        pos = event.position()
        if self._left_arrow_rect().contains(pos):
            self._prev()
        elif self._right_arrow_rect().contains(pos):
            self._next()
        else:
            for i, rect in enumerate(self._dot_rects()):
                if rect.contains(pos):
                    self._current_index = i
                    self.update()
                    break

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_arrow = 0
        if self._left_arrow_rect().contains(pos):
            self._hovered_arrow = -1
        elif self._right_arrow_rect().contains(pos):
            self._hovered_arrow = 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#1E1E1E") if is_dark else QColor("#F5F5F5")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        arrow_bg = QColor("#3D3D3D") if is_dark else QColor("#E0E0E0")
        arrow_hover = QColor("#505050") if is_dark else QColor("#CCCCCC")
        dot_inactive = QColor("#555555") if is_dark else QColor("#BBBBBB")
        dot_active = QColor("#0078D4")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        if self._items:
            item = self._items[self._current_index]
            content_rect = QRectF(48, 8, self.width() - 96, self.height() - 40)
            painter.setBrush(QColor(item.get("color", "#0078D4")))
            painter.drawRoundedRect(content_rect, 8, 8)

            title = item.get("title", "")
            painter.setPen(text_color)
            font = painter.font()
            font.setPointSize(14)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(content_rect, Qt.AlignmentFlag.AlignCenter, title)

        left_rect = self._left_arrow_rect()
        painter.setBrush(arrow_hover if self._hovered_arrow == -1 else arrow_bg)
        painter.drawRoundedRect(left_rect, 6, 6)
        left_icon = FIF.LEFT_ARROW.icon()
        painter.drawPixmap(int(left_rect.x() + 6), int(left_rect.y() + 6), left_icon.pixmap(20, 20))

        right_rect = self._right_arrow_rect()
        painter.setBrush(arrow_hover if self._hovered_arrow == 1 else arrow_bg)
        painter.drawRoundedRect(right_rect, 6, 6)
        right_icon = FIF.RIGHT_ARROW.icon()
        painter.drawPixmap(int(right_rect.x() + 6), int(right_rect.y() + 6), right_icon.pixmap(20, 20))

        for i, dot_rect in enumerate(self._dot_rects()):
            painter.setBrush(dot_active if i == self._current_index else dot_inactive)
            painter.drawEllipse(dot_rect)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
