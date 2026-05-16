from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class CountdownTimer(QWidget):
    finished = Signal()

    def __init__(self, seconds=300, parent=None):
        super().__init__(parent)
        self._total_seconds = seconds
        self._remaining = seconds
        self._flip_progress = 1.0
        self._running = False
        self.setFixedSize(160, 80)
        self._flip_anim = QPropertyAnimation(self, b"flipProgress")
        self._flip_anim.setDuration(300)
        self._flip_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

    def get_flip_progress(self):
        return self._flip_progress

    def set_flip_progress(self, val):
        self._flip_progress = val
        self.update()

    flipProgress = Property(float, get_flip_progress, set_flip_progress)

    def start(self):
        self._running = True
        self._timer.start()

    def pause(self):
        self._running = False
        self._timer.stop()

    def reset(self):
        self._running = False
        self._timer.stop()
        self._remaining = self._total_seconds
        self.update()

    def _tick(self):
        if self._remaining <= 0:
            self._timer.stop()
            self._running = False
            self.finished.emit()
            return
        self._remaining -= 1
        self._flip_progress = 0.0
        self._flip_anim.stop()
        self._flip_anim.setStartValue(0.0)
        self._flip_anim.setEndValue(1.0)
        self._flip_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg_color = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#888888") if dark else QColor("#666666")
        ring_bg = QColor("#404040") if dark else QColor("#E0E0E0")
        accent = QColor("#0078D4")
        w, h = self.width(), self.height()
        card_r = 10
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(QRectF(0, 0, w, h), card_r, card_r)
        ring_cx = 30
        ring_cy = h / 2
        ring_r = 22
        pen = QPen(ring_bg, 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(int(ring_cx - ring_r), int(ring_cy - ring_r), ring_r * 2, ring_r * 2, 0, 360 * 16)
        progress = self._remaining / max(self._total_seconds, 1)
        span = int(-progress * 360 * 16)
        pen = QPen(accent, 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(int(ring_cx - ring_r), int(ring_cy - ring_r), ring_r * 2, ring_r * 2, 90 * 16, span)
        mins = self._remaining // 60
        secs = self._remaining % 60
        time_str = f"{mins:02d}:{secs:02d}"
        flip_y_offset = (1.0 - self._flip_progress) * 4
        painter.setPen(text_color)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        painter.setFont(font)
        text_rect = QRectF(58, h / 2 - 20 + flip_y_offset, 96, 28)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, time_str)
        painter.setPen(sub_color)
        font.setPointSize(8)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(QRectF(58, h / 2 + 10, 96, 16), Qt.AlignmentFlag.AlignCenter, "remaining")
        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self._running:
            self._timer.start()
        if self._flip_anim.state() == QPropertyAnimation.State.Paused:
            self._flip_anim.resume()

    def hideEvent(self, event):
        if self._timer.isActive():
            self._timer.stop()
        if self._flip_anim.state() == QPropertyAnimation.State.Running:
            self._flip_anim.pause()
        super().hideEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
