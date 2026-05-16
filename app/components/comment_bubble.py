from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class CommentBubble(QWidget):
    def __init__(self, text="", author="", timestamp="", is_own=False, parent=None):
        super().__init__(parent)
        self._text = text
        self._author = author
        self._timestamp = timestamp
        self._is_own = is_own
        self._progress = 0.0
        self._anim = QPropertyAnimation(self, b"progress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setMinimumWidth(200)
        self.setMinimumHeight(60)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_progress(self):
        return self._progress

    def set_progress(self, val):
        self._progress = val
        self.update()

    progress = Property(float, get_progress, set_progress)

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.update()

    def get_author(self):
        return self._author

    def set_author(self, author):
        self._author = author
        self.update()

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, ts):
        self._timestamp = ts
        self.update()

    def sizeHint(self):
        return self.minimumSize()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        alpha = self._progress
        painter.setOpacity(alpha)
        offset_y = (1.0 - alpha) * 10
        painter.translate(0, offset_y)
        w = self.width()
        h = self.height()
        tail_w = 8
        tail_h = 10
        radius = 12
        if self._is_own:
            bubble_rect = QRectF(0, 0, w - tail_w, h)
            bubble_bg = QColor("#0078D4")
            text_color = QColor("#FFFFFF")
            author_color = QColor("#CCDDFF")
            time_color = QColor("#99BBFF")
        else:
            bubble_rect = QRectF(tail_w, 0, w - tail_w, h)
            bubble_bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
            text_color = QColor("#D4D4D4") if is_dark else QColor("#1A1A1A")
            author_color = QColor("#60CDFF") if is_dark else QColor("#0078D4")
            time_color = QColor("#888888") if is_dark else QColor("#9E9E9E")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bubble_bg)
        painter.drawRoundedRect(bubble_rect, radius, radius)
        tail_path = QPainterPath()
        if self._is_own:
            tail_path.moveTo(w - tail_w, h * 0.3)
            tail_path.lineTo(w, h * 0.3 + tail_h / 2)
            tail_path.lineTo(w - tail_w, h * 0.3 + tail_h)
            tail_path.closeSubpath()
        else:
            tail_path.moveTo(tail_w, h * 0.3)
            tail_path.lineTo(0, h * 0.3 + tail_h / 2)
            tail_path.lineTo(tail_w, h * 0.3 + tail_h)
            tail_path.closeSubpath()
        painter.drawPath(tail_path)
        padding = 14
        if self._is_own:
            text_x = padding
        else:
            text_x = tail_w + padding
        text_w = w - tail_w - padding * 2
        font = QFont()
        if self._author:
            font.setPixelSize(11)
            font.setWeight(QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(author_color)
            author_rect = QRectF(text_x, 8, text_w, 16)
            painter.drawText(author_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, self._author)
            text_top = 26
        else:
            text_top = 10
        font.setPixelSize(12)
        font.setWeight(QFont.Weight.Normal)
        painter.setFont(font)
        painter.setPen(text_color)
        text_rect = QRectF(text_x, text_top, text_w, h - text_top - 20)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextWordWrap, self._text)
        if self._timestamp:
            font.setPixelSize(10)
            painter.setFont(font)
            painter.setPen(time_color)
            time_rect = QRectF(text_x, h - 18, text_w, 14)
            painter.drawText(time_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom, self._timestamp)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
