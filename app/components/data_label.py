from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class DataLabel(QWidget):
    def __init__(self, text="", color="#0078D4", parent=None):
        super().__init__(parent)
        self._text = text
        self._color = color
        self._progress = 0.0
        self._anim = QPropertyAnimation(self, b"labelProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setMinimumSize(44, 28)

    def _is_dark(self):
        return isDarkTheme()

    def get_progress(self):
        return self._progress

    def set_progress(self, val):
        self._progress = val
        self.update()

    labelProgress = Property(float, get_progress, set_progress)

    def set_text(self, text):
        self._text = text
        self._progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def set_color(self, color):
        self._color = color
        self.update()

    def show_animated(self):
        self._progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        text_color = QColor("#1A1A1A") if not is_dark else QColor("#FFFFFF")

        p = self._progress
        alpha = p
        y_offset = (1.0 - p) * 8

        painter.setOpacity(alpha)

        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)

        fm = painter.fontMetrics()
        text_w = fm.horizontalAdvance(self._text)
        text_h = fm.height()
        pill_w = text_w + 20
        pill_h = text_h + 10
        pill_x = (self.width() - pill_w) / 2
        pill_y = (self.height() - pill_h) / 2 + y_offset

        accent = QColor(self._color)
        accent.setAlpha(int(30 * p))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(accent)
        painter.drawRoundedRect(QRectF(pill_x, pill_y, pill_w, pill_h), pill_h / 2, pill_h / 2)

        text_rect = QRectF(pill_x, pill_y, pill_w, pill_h)
        painter.setPen(text_color)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._text)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
