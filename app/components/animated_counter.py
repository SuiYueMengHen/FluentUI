from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QFont


class AnimatedCounter(QWidget):
    def __init__(self, parent=None, prefix="", suffix="", font_size=36):
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0
        self._prefix = prefix
        self._suffix = suffix
        self._font_size = font_size

        self.setMinimumSize(80, 50)

        self._anim = QPropertyAnimation(self, b"displayValue")
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def get_display_value(self):
        return self._display_value

    def set_display_value(self, val):
        self._display_value = val
        self.update()

    displayValue = Property(float, get_display_value, set_display_value)

    def set_value(self, value):
        self._value = value
        self._anim.setStartValue(self._display_value)
        self._anim.setEndValue(float(value))
        self._anim.start()

    def get_value(self):
        return self._value

    def set_prefix(self, prefix):
        self._prefix = prefix
        self.update()

    def set_suffix(self, suffix):
        self._suffix = suffix
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

        font = QFont()
        font.setPixelSize(self._font_size)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)

        display_int = int(round(self._display_value))
        text = f"{self._prefix}{display_int}{self._suffix}"

        painter.drawText(
            QRectF(0, 0, self.width(), self.height()),
            Qt.AlignmentFlag.AlignCenter,
            text
        )

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
