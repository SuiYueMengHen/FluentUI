from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme, IconWidget


class FollowButton(QWidget):
    followChanged = Signal(bool)

    def __init__(self, following=False, parent=None):
        super().__init__(parent)
        self._following = following
        self._progress = 0.0
        self._hover = False
        self._anim = QPropertyAnimation(self, b"progress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(100, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def get_progress(self):
        return self._progress

    def set_progress(self, val):
        self._progress = val
        self.update()

    progress = Property(float, get_progress, set_progress)

    def is_following(self):
        return self._following

    def set_following(self, following):
        if following != self._following:
            self._following = following
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(1.0)
            self._anim.start()
            self.followChanged.emit(following)
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
            self.set_following(not self._following)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        rect = QRectF(0, 0, self.width(), self.height())
        radius = 18
        if self._following:
            border_color = QColor("#0078D4") if not self._hover else QColor("#FF4444")
            bg_color = QColor("#0078D4") if is_dark else QColor("transparent")
            if self._hover:
                bg_color = QColor("#3D0000") if is_dark else QColor("#FFEEEE")
            text_color = QColor("#FF4444") if self._hover else (QColor("#0078D4") if not is_dark else QColor("#60CDFF"))
            text = "Unfollow" if self._hover else "Following"
            painter.setPen(QPen(border_color, 1.5))
            painter.setBrush(bg_color)
            painter.drawRoundedRect(rect, radius, radius)
            painter.setPen(text_color)
            font = QFont()
            font.setPixelSize(12)
            font.setWeight(QFont.Weight.Medium)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
        else:
            bg_color = QColor("#0078D4")
            if self._hover:
                bg_color = bg_color.darker(110)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(bg_color)
            painter.drawRoundedRect(rect, radius, radius)
            icon = FIF.PEOPLE
            icon_pixmap = icon.icon().pixmap(14, 14)
            icon_x = int(self.width() / 2 - 38)
            icon_y = int((self.height() - 14) / 2)
            painter.drawPixmap(icon_x, icon_y, icon_pixmap)
            painter.setPen(QColor("#FFFFFF"))
            font = QFont()
            font.setPixelSize(12)
            font.setWeight(QFont.Weight.Medium)
            painter.setFont(font)
            painter.drawText(rect.adjusted(14, 0, 0, 0), Qt.AlignmentFlag.AlignCenter, "Follow")
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
