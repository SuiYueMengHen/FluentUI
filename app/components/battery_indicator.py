from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class BatteryIndicator(QWidget):
    def __init__(self, level=75, parent=None):
        super().__init__(parent)
        self._level = level
        self._fill_level = 0.0
        self.setFixedSize(80, 40)
        self._anim = QPropertyAnimation(self, b"fillLevel")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(float(level))
        self._anim.start()

    def get_fill_level(self):
        return self._fill_level

    def set_fill_level(self, val):
        self._fill_level = val
        self.update()

    fillLevel = Property(float, get_fill_level, set_fill_level)

    def set_level(self, level):
        self._level = max(0, min(100, level))
        self._anim.stop()
        self._anim.setStartValue(self._fill_level)
        self._anim.setEndValue(float(self._level))
        self._anim.start()

    def _get_color(self, level):
        if level > 50:
            return QColor("#0F7B0F")
        elif level > 20:
            return QColor("#9D5D00")
        else:
            return QColor("#C42B1C")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        outline_color = QColor("#CCCCCC") if not dark else QColor("#606060")
        text_color = QColor("#1A1A1A") if not dark else QColor("#FFFFFF")
        body_x, body_y = 5, 8
        body_w, body_h = 58, 24
        cap_x = body_x + body_w
        cap_y = body_y + 6
        cap_w, cap_h = 6, 12
        pen = QPen(outline_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(body_x, body_y, body_w, body_h), 3, 3)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(outline_color)
        painter.drawRoundedRect(QRectF(cap_x, cap_y, cap_w, cap_h), 2, 2)
        fill_w = (body_w - 6) * (self._fill_level / 100.0)
        if fill_w > 0:
            fill_color = self._get_color(self._fill_level)
            painter.setBrush(fill_color)
            painter.drawRoundedRect(QRectF(body_x + 3, body_y + 3, fill_w, body_h - 6), 2, 2)
        painter.setPen(text_color)
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(body_x, body_y, body_w, body_h), Qt.AlignmentFlag.AlignCenter, f"{int(self._fill_level)}%")
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
