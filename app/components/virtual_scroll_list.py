from PySide6.QtWidgets import QWidget, QScrollBar
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QWheelEvent
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class VirtualScrollList(QWidget):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._items = list(items or [])
        self._fade_progress = 1.0
        self._scroll_offset = 0
        self._item_height = 32
        self._fade_anim = QPropertyAnimation(self, b"fadeProgress")
        self._fade_anim.setDuration(150)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedWidth(260)
        self.setMinimumHeight(200)

    def get_fade_progress(self):
        return self._fade_progress

    def set_fade_progress(self, val):
        self._fade_progress = val
        self.update()

    fadeProgress = Property(float, get_fade_progress, set_fade_progress)

    def set_items(self, items):
        self._items = list(items)
        self._scroll_offset = 0
        self._fade_progress = 0.0
        self._fade_anim.stop()
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def _max_scroll(self):
        total = len(self._items) * self._item_height
        visible = self.height() - 4
        return max(0, total - visible)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self._scroll_offset -= delta
        self._scroll_offset = max(0, min(self._max_scroll(), self._scroll_offset))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#888888")
        item_bg = QColor("#353535") if dark else QColor("#F8F8F8")
        scroll_bg = QColor("#404040") if dark else QColor("#E0E0E0")
        scroll_fg = QColor("#606060") if dark else QColor("#C0C0C0")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
        clip_rect = QRectF(2, 2, self.width() - 18, self.height() - 4)
        painter.setClipRect(clip_rect)
        start_idx = int(self._scroll_offset / self._item_height)
        visible_count = int(self.height() / self._item_height) + 2
        end_idx = min(start_idx + visible_count, len(self._items))
        for i in range(start_idx, end_idx):
            y = 2 + i * self._item_height - self._scroll_offset
            if y + self._item_height < 2 or y > self.height():
                continue
            rect = QRectF(4, y, self.width() - 22, self._item_height - 2)
            painter.setBrush(item_bg)
            painter.drawRoundedRect(rect, 4, 4)
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            painter.setOpacity(self._fade_progress)
            painter.drawText(QRectF(14, y, self.width() - 34, self._item_height - 2), Qt.AlignmentFlag.AlignVCenter, self._items[i])
            painter.setOpacity(1.0)
        painter.setClipping(False)
        if self._max_scroll() > 0:
            sb_x = self.width() - 12
            sb_h = self.height() - 4
            painter.setBrush(scroll_bg)
            painter.drawRoundedRect(QRectF(sb_x, 2, 8, sb_h), 4, 4)
            ratio = self.height() / max(len(self._items) * self._item_height, 1)
            thumb_h = max(20, sb_h * ratio)
            thumb_y = 2 + (sb_h - thumb_h) * (self._scroll_offset / max(self._max_scroll(), 1))
            painter.setBrush(scroll_fg)
            painter.drawRoundedRect(QRectF(sb_x, thumb_y, 8, thumb_h), 4, 4)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
