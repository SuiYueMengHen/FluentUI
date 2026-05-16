from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme, IconWidget


class MiniStat(QWidget):
    def __init__(self, value="0", label="", trend="", icon=FIF.INFO, accent_color="#0078D4", parent=None):
        super().__init__(parent)
        self._value = value
        self._label = label
        self._trend = trend
        self._icon = icon
        self._accent_color = accent_color
        self._value_progress = 0.0
        self._anim = QPropertyAnimation(self, b"valueProgress")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(160, 80)

    def _is_dark(self):
        return isDarkTheme()

    def get_value_progress(self):
        return self._value_progress

    def set_value_progress(self, val):
        self._value_progress = val
        self.update()

    valueProgress = Property(float, get_value_progress, set_value_progress)

    def set_value(self, value):
        self._value = str(value)
        self._value_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def show_animated(self):
        self._value_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg = QColor("#FFFFFF") if not is_dark else QColor("#2D2D2D")
        border = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")
        text_color = QColor("#1A1A1A") if not is_dark else QColor("#FFFFFF")
        dim_color = QColor("#616161") if not is_dark else QColor("#9E9E9E")

        r = QRectF(0, 0, self.width(), self.height())
        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(r, 10, 10)

        p = self._value_progress
        painter.setOpacity(p)

        icon_w = 24
        icon_h = 24
        icon_x = 14
        icon_y = 14
        icon_rect = QRectF(icon_x, icon_y, icon_w, icon_h)
        accent = QColor(self._accent_color)
        accent.setAlpha(int(40 * p))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(accent)
        painter.drawRoundedRect(icon_rect, 4, 4)

        icon_pixmap = self._icon.icon().pixmap(int(icon_w), int(icon_h))
        painter.setOpacity(p)
        painter.drawPixmap(int(icon_x), int(icon_y), icon_pixmap)

        font = painter.font()
        font.setPointSize(18)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        value_rect = QRectF(14, 40, self.width() - 28, 24)
        painter.drawText(value_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._value)

        if self._trend:
            font.setPointSize(10)
            font.setBold(False)
            painter.setFont(font)
            trend_positive = "+" in self._trend or "↑" in self._trend
            trend_color = QColor("#4CAF50") if trend_positive else QColor("#F44336")
            painter.setPen(trend_color)
            trend_rect = QRectF(self.width() - 60, 14, 46, 20)
            painter.drawText(trend_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._trend)

        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(dim_color)
        label_rect = QRectF(14, 62, self.width() - 28, 16)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._label)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
