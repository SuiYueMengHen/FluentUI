from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QFontMetrics
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class GradientText(QWidget):
    def __init__(self, text="", color1="#0078D4", color2="#005A9E", parent=None):
        super().__init__(parent)
        self._text = text
        self._color1 = color1
        self._color2 = color2
        self._gradient_offset = 0.0
        self.setFixedHeight(40)
        self._anim = QPropertyAnimation(self, b"gradientOffset")
        self._anim.setDuration(3000)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Type.Linear)
        self._update_size()

    def sizeHint(self):
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        fm = QFontMetrics(font)
        text_w = fm.horizontalAdvance(self._text) if self._text else 0
        return QSize(max(text_w + 20, 60), 40)

    def _update_size(self):
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        fm = QFontMetrics(font)
        text_w = fm.horizontalAdvance(self._text) if self._text else 0
        self.setFixedWidth(max(text_w + 20, 60))

    def showEvent(self, event):
        super().showEvent(event)
        self._anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._anim.stop()

    def get_gradient_offset(self):
        return self._gradient_offset

    def set_gradient_offset(self, val):
        self._gradient_offset = val
        self.update()

    gradientOffset = Property(float, get_gradient_offset, set_gradient_offset)

    def set_text(self, text):
        self._text = text
        self._update_size()
        self.update()

    def set_colors(self, color1, color2):
        self._color1 = color1
        self._color2 = color2
        self.update()

    def paintEvent(self, event):
        if not self._text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        c1 = QColor(self._color1)
        c2 = QColor(self._color2)
        if dark:
            c1 = c1.lighter(120)
            c2 = c2.lighter(150)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        painter.setFont(font)
        fm = painter.fontMetrics()
        text_w = fm.horizontalAdvance(self._text)
        text_h = fm.height()
        x_offset = (self.width() - text_w) / 2
        y_offset = (self.height() - text_h) / 2 + fm.ascent()
        offset = self._gradient_offset
        gradient = QLinearGradient()
        grad_start = -text_w + offset * text_w * 3
        grad_end = grad_start + text_w * 2
        gradient.setStart(grad_start + x_offset, 0)
        gradient.setFinalStop(grad_end + x_offset, 0)
        gradient.setColorAt(0, c1)
        gradient.setColorAt(0.5, c2)
        gradient.setColorAt(1, c1)
        painter.setPen(QPen(QBrush(gradient), 1))
        painter.drawText(int(x_offset), int(y_offset), self._text)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
