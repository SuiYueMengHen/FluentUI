from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class SignalStrength(QWidget):
    def __init__(self, strength=3, parent=None):
        super().__init__(parent)
        self._strength = max(0, min(4, strength))
        self._anim_progress = 0.0
        self.setFixedSize(40, 32)
        self._anim = QPropertyAnimation(self, b"animProgress")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._first_show = True

    def get_anim_progress(self):
        return self._anim_progress

    def set_anim_progress(self, val):
        self._anim_progress = val
        self.update()

    animProgress = Property(float, get_anim_progress, set_anim_progress)

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self._anim.start()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.pause()
        super().hideEvent(event)

    def set_strength(self, strength):
        self._strength = max(0, min(4, strength))
        self._anim.stop()
        self._anim_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        filled_color = QColor("#0078D4")
        empty_color = QColor("#404040") if dark else QColor("#E0E0E0")
        bar_w = 6
        gap = 3
        base_y = self.height() - 4
        heights = [6, 12, 18, 24]
        for i in range(4):
            h = heights[i]
            x = 4 + i * (bar_w + gap)
            y = base_y - h
            is_filled = i < self._strength
            if is_filled and self._anim_progress < 1.0:
                threshold = (i + 1) / 4.0
                if self._anim_progress >= threshold:
                    painter.setBrush(filled_color)
                else:
                    partial = max(0.0, (self._anim_progress - i / 4.0) * 4.0)
                    if partial > 0:
                        painter.setBrush(filled_color)
                    else:
                        painter.setBrush(empty_color)
            elif is_filled:
                painter.setBrush(filled_color)
            else:
                painter.setBrush(empty_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_w, h), 2, 2)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
