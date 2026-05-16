from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class VideoThumbnail(QWidget):
    def __init__(self, title="", duration="3:45", color="#333333", parent=None):
        super().__init__(parent)
        self._title = title
        self._duration = duration
        self._color = color
        self._scale = 1.0
        self._hovered = False
        self.setFixedSize(240, 160)
        self.setMouseTracking(True)

        self._scale_anim = QPropertyAnimation(self, b"scaleFactor")
        self._scale_anim.setDuration(150)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_scale_factor(self):
        return self._scale

    def set_scale_factor(self, val):
        self._scale = val
        self.update()

    scaleFactor = Property(float, get_scale_factor, set_scale_factor)

    def _is_dark(self):
        return isDarkTheme()

    def enterEvent(self, event):
        self._hovered = True
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(1.03)
        self._scale_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(1.0)
        self._scale_anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        play_bg = QColor(255, 255, 255, 180) if is_dark else QColor(255, 255, 255, 200)
        play_icon_color = QColor("#1A1A1A")

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2

        painter.translate(cx, cy)
        painter.scale(self._scale, self._scale)
        painter.translate(-cx, -cy)

        thumb_rect = QRectF(0, 0, w, h)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self._color))
        painter.drawRoundedRect(thumb_rect, 8, 8)

        play_radius = 24
        play_rect = QRectF(cx - play_radius, cy - play_radius, play_radius * 2, play_radius * 2)
        painter.setBrush(play_bg)
        painter.drawEllipse(play_rect)

        icon = FIF.PLAY.icon()
        pixmap = icon.pixmap(22, 22)
        painter.drawPixmap(int(cx - 11), int(cy - 11), pixmap)

        badge_w = 40
        badge_h = 20
        badge_rect = QRectF(w - badge_w - 8, h - badge_h - 8, badge_w, badge_h)
        painter.setBrush(QColor(0, 0, 0, 160))
        painter.drawRoundedRect(badge_rect, 4, 4)

        painter.setPen(QColor("#FFFFFF"))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, self._duration)

        if self._title:
            title_rect = QRectF(8, 8, w - 16, 20)
            painter.setPen(text_color)
            font.setPointSize(10)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._title)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
