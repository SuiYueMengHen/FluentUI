from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class StatusPill(QWidget):
    STATUS_COLORS = {
        "info": "#0078D4",
        "success": "#0F7B0F",
        "warning": "#9D5D00",
        "error": "#C42B1C",
    }

    def __init__(self, text="", status="info", parent=None):
        super().__init__(parent)
        self._text = text
        self._status = status
        self._color_progress = 1.0
        self._prev_status = status
        self.setFixedHeight(26)
        self._anim = QPropertyAnimation(self, b"colorProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._update_size()

    def sizeHint(self):
        pill_w = max(60, len(self._text) * 8 + 36)
        return QSize(int(pill_w), 26)

    def _update_size(self):
        pill_w = max(60, len(self._text) * 8 + 36)
        self.setFixedWidth(int(pill_w))

    def get_color_progress(self):
        return self._color_progress

    def set_color_progress(self, val):
        self._color_progress = val
        self.update()

    colorProgress = Property(float, get_color_progress, set_color_progress)

    def set_status(self, status):
        self._prev_status = self._status
        self._status = status
        self._color_progress = 0.0
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def set_text(self, text):
        self._text = text
        self._update_size()
        self.update()

    def _get_bg_color(self, status_color, dark):
        c = QColor(status_color)
        if dark:
            c.setAlpha(40)
        else:
            c.setAlpha(30)
        return c

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        status_color = self.STATUS_COLORS.get(self._status, "#0078D4")
        color = QColor(status_color)
        bg = self._get_bg_color(status_color, dark)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), self.height() / 2, self.height() / 2)
        dot_r = 4
        dot_cx = 14
        dot_cy = self.height() / 2
        painter.setBrush(color)
        painter.drawEllipse(QRectF(dot_cx - dot_r, dot_cy - dot_r, dot_r * 2, dot_r * 2))
        painter.setPen(text_color)
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        painter.drawText(QRectF(24, 0, self.width() - 30, self.height()), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
