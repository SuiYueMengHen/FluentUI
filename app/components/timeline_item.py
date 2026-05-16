from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class TimelineItem(QWidget):
    def __init__(self, title="", description="", timestamp="", color="#0078D4", parent=None):
        super().__init__(parent)
        self._title = title
        self._description = description
        self._timestamp = timestamp
        self._color = color
        self._pulse_progress = 0.0

        self.setMinimumHeight(80)
        self.setMinimumWidth(200)

        self._anim = QPropertyAnimation(self, b"pulseProgress")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setLoopCount(-1)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)

    def showEvent(self, event):
        super().showEvent(event)
        self._anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._anim.stop()

    def get_pulse_progress(self):
        return self._pulse_progress

    def set_pulse_progress(self, val):
        self._pulse_progress = val
        self.update()

    pulseProgress = Property(float, get_pulse_progress, set_pulse_progress)

    def refresh_theme(self):
        self.update()

    def _is_dark(self):
        return isDarkTheme()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self._is_dark()
        line_color = QColor("#444444") if dark else QColor("#DDDDDD")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        desc_color = QColor("#AAAAAA") if dark else QColor("#666666")
        time_color = QColor("#888888") if dark else QColor("#999999")
        dot_color = QColor(self._color)

        dot_x = 20
        dot_y = 20
        dot_r = 6

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(line_color)
        painter.drawRect(int(dot_x - 1), int(dot_y + dot_r), 2, self.height() - dot_y - dot_r)

        painter.drawRect(int(dot_x - 1), 0, 2, int(dot_y - dot_r))

        pulse_r = dot_r + 8 * self._pulse_progress
        pulse_alpha = int(80 * (1 - self._pulse_progress))
        pulse_color = QColor(dot_color)
        pulse_color.setAlpha(pulse_alpha)
        painter.setBrush(pulse_color)
        painter.drawEllipse(QRectF(dot_x - pulse_r, dot_y - pulse_r, pulse_r * 2, pulse_r * 2))

        painter.setBrush(dot_color)
        painter.drawEllipse(QRectF(dot_x - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2))

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        title_rect = QRectF(40, 8, self.width() - 50, 22)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._title)

        font.setPointSize(9)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(desc_color)
        desc_rect = QRectF(40, 30, self.width() - 50, 20)
        painter.drawText(desc_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._description)

        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(time_color)
        time_rect = QRectF(40, 50, self.width() - 50, 18)
        painter.drawText(time_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._timestamp)

        painter.end()
