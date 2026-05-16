from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QConicalGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class PullRefresh(QWidget):
    refreshRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pull_offset = 0.0
        self._refreshing = False
        self._spinner_angle = 0
        self.setFixedHeight(60)
        self._anim = QPropertyAnimation(self, b"pullOffset")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._spinner_timer = QTimer(self)
        self._spinner_timer.timeout.connect(self._spin_tick)

    def get_pull_offset(self):
        return self._pull_offset

    def set_pull_offset(self, val):
        self._pull_offset = val
        self.update()

    pullOffset = Property(float, get_pull_offset, set_pull_offset)

    def set_refreshing(self, refreshing):
        self._refreshing = refreshing
        if refreshing:
            self._spinner_timer.start(30)
        else:
            self._spinner_timer.stop()
            self._spinner_angle = 0
            self._pull_offset = 0.0
            self._anim.stop()
            self._anim.setStartValue(self._pull_offset)
            self._anim.setEndValue(0.0)
            self._anim.start()

    def _spin_tick(self):
        self._spinner_angle = (self._spinner_angle + 10) % 360
        self.update()

    def trigger_refresh(self):
        self._refreshing = True
        self._pull_offset = 40.0
        self._spinner_timer.start(30)
        self.refreshRequested.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        accent = QColor("#0078D4")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#888888")
        cx = self.width() / 2
        cy = 10 + self._pull_offset * 0.6
        if self._refreshing:
            spinner_r = 12
            pen = QPen(accent, 3)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawArc(int(cx - spinner_r), int(cy - spinner_r), spinner_r * 2, spinner_r * 2, self._spinner_angle * 16, 270 * 16)
            painter.setPen(sub_color)
            font = QFont()
            font.setPointSize(8)
            painter.setFont(font)
            painter.drawText(QRectF(cx - 40, cy + 16, 80, 16), Qt.AlignmentFlag.AlignCenter, "Refreshing...")
        else:
            arrow_size = 16
            FIF.DOWN.icon().paint(painter, QRectF(cx - arrow_size / 2, cy - arrow_size / 2, arrow_size, arrow_size).toRect())
            if self._pull_offset > 20:
                painter.setPen(accent)
                font = QFont()
                font.setPointSize(8)
                painter.setFont(font)
                painter.drawText(QRectF(cx - 50, cy + 12, 100, 16), Qt.AlignmentFlag.AlignCenter, "Release to refresh")
            else:
                painter.setPen(sub_color)
                font = QFont()
                font.setPointSize(8)
                painter.setFont(font)
                painter.drawText(QRectF(cx - 50, cy + 12, 100, 16), Qt.AlignmentFlag.AlignCenter, "Pull to refresh")
        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self._refreshing:
            self._spinner_timer.start(30)
        if self._anim.state() == QPropertyAnimation.State.Paused:
            self._anim.resume()

    def hideEvent(self, event):
        if self._spinner_timer.isActive():
            self._spinner_timer.stop()
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.pause()
        super().hideEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
