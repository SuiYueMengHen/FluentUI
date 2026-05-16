from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class KanbanCard(QFrame):
    PRIORITY_COLORS = {
        "high": "#C42B1C",
        "medium": "#9D5D00",
        "low": "#0F7B0F",
    }

    def __init__(self, title="", description="", priority="medium", tags=None, parent=None):
        super().__init__(parent)
        self._title = title
        self._description = description
        self._priority = priority
        self._tags = tags or []
        self._drag_scale = 1.0
        self._pressed = False

        self.setMinimumWidth(180)
        self.setMinimumHeight(90)
        self.setMaximumWidth(260)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        self._anim = QPropertyAnimation(self, b"dragScale")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_drag_scale(self):
        return self._drag_scale

    def set_drag_scale(self, val):
        self._drag_scale = val
        self.update()

    dragScale = Property(float, get_drag_scale, set_drag_scale)

    def refresh_theme(self):
        self.update()

    def _is_dark(self):
        return isDarkTheme()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self._anim.setStartValue(self._drag_scale)
            self._anim.setEndValue(0.95)
            self._anim.start()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            self._anim.setStartValue(self._drag_scale)
            self._anim.setEndValue(1.0)
            self._anim.start()
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self._is_dark()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border_color = QColor("#444444") if dark else QColor("#DDDDDD")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        desc_color = QColor("#AAAAAA") if dark else QColor("#666666")
        tag_bg = QColor("#3A3A3A") if dark else QColor("#F0F0F0")
        tag_text = QColor("#CCCCCC") if dark else QColor("#444444")

        scale = self._drag_scale
        cx = self.width() / 2
        cy = self.height() / 2
        sw = self.width() * scale
        sh = self.height() * scale

        painter.translate(cx, cy)
        painter.scale(scale, scale)
        painter.translate(-cx, -cy)

        card_rect = QRectF(0, 0, self.width(), self.height())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(card_rect, 10, 10)

        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(card_rect, 10, 10)

        priority_color = QColor(self.PRIORITY_COLORS.get(self._priority, "#9D5D00"))
        strip_rect = QRectF(0, 0, 4, self.height())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(priority_color)
        path = QPainterPath()
        path.addRoundedRect(card_rect, 10, 10)
        clip_path = QPainterPath()
        clip_path.addRect(QRectF(0, 0, 4, self.height()))
        painter.setClipPath(path.intersected(clip_path))
        painter.drawRoundedRect(card_rect, 10, 10)
        painter.setClipping(False)

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        title_rect = QRectF(14, 10, self.width() - 24, 20)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._title)

        font.setPointSize(9)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(desc_color)
        desc_rect = QRectF(14, 32, self.width() - 24, 20)
        elided = self._description[:60] + "..." if len(self._description) > 60 else self._description
        painter.drawText(desc_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

        if self._tags:
            tag_x = 14
            tag_y = 56
            font.setPointSize(8)
            painter.setFont(font)
            for tag in self._tags[:3]:
                tag_w = max(40, len(tag) * 8 + 12)
                tag_rect = QRectF(tag_x, tag_y, tag_w, 20)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(tag_bg)
                painter.drawRoundedRect(tag_rect, 4, 4)
                painter.setPen(tag_text)
                painter.drawText(tag_rect, Qt.AlignmentFlag.AlignCenter, tag)
                tag_x += tag_w + 6

        painter.end()
