from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class StickyHeader(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        self._shadow_opacity = 0.0
        self._scrolled = False
        self.setFixedHeight(48)
        self._anim = QPropertyAnimation(self, b"shadowOpacity")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_shadow_opacity(self):
        return self._shadow_opacity

    def set_shadow_opacity(self, val):
        self._shadow_opacity = val
        self.update()

    shadowOpacity = Property(float, get_shadow_opacity, set_shadow_opacity)

    def set_scrolled(self, scrolled):
        self._scrolled = scrolled
        self._anim.stop()
        self._anim.setStartValue(self._shadow_opacity)
        self._anim.setEndValue(1.0 if scrolled else 0.0)
        self._anim.start()

    def set_title(self, title):
        self._title = title
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRect(QRectF(0, 0, self.width(), self.height()))
        if self._shadow_opacity > 0:
            shadow_color = QColor(0, 0, 0, int(40 * self._shadow_opacity)) if not dark else QColor(0, 0, 0, int(60 * self._shadow_opacity))
            gradient = QLinearGradient(0, self.height(), 0, self.height() + 8)
            gradient.setColorAt(0, shadow_color)
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(gradient)
            painter.drawRect(QRectF(0, self.height(), self.width(), 8))
        FIF.LEFT_ARROW.icon().paint(painter, QRectF(12, (self.height() - 20) / 2, 20, 20).toRect())
        painter.setPen(text_color)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(40, 0, self.width() - 52, self.height()), Qt.AlignmentFlag.AlignVCenter, self._title)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
