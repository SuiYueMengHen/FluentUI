from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class StepperInput(QWidget):
    valueChanged = Signal(int)

    def __init__(self, value=0, min_val=0, max_val=999, parent=None):
        super().__init__(parent)
        self._value = value
        self._min_val = min_val
        self._max_val = max_val
        self._scroll_offset = 0.0
        self._prev_value = value
        self._hovered_btn = 0
        self.setFixedSize(140, 40)

        self._scroll_anim = QPropertyAnimation(self, b"scrollOffset")
        self._scroll_anim.setDuration(200)
        self._scroll_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_scroll_offset(self):
        return self._scroll_offset

    def set_scroll_offset(self, val):
        self._scroll_offset = val
        self.update()

    scrollOffset = Property(float, get_scroll_offset, set_scroll_offset)

    def _is_dark(self):
        return isDarkTheme()

    def _minus_rect(self):
        return QRectF(0, 0, 36, 40)

    def _plus_rect(self):
        return QRectF(104, 0, 36, 40)

    def _value_rect(self):
        return QRectF(36, 0, 68, 40)

    def _increment(self):
        if self._value < self._max_val:
            self._prev_value = self._value
            self._value += 1
            self._scroll_anim.setStartValue(1.0)
            self._scroll_anim.setEndValue(0.0)
            self._scroll_anim.start()
            self.valueChanged.emit(self._value)

    def _decrement(self):
        if self._value > self._min_val:
            self._prev_value = self._value
            self._value -= 1
            self._scroll_anim.setStartValue(-1.0)
            self._scroll_anim.setEndValue(0.0)
            self._scroll_anim.start()
            self.valueChanged.emit(self._value)

    def mousePressEvent(self, event):
        pos = event.position()
        if self._minus_rect().contains(pos):
            self._decrement()
        elif self._plus_rect().contains(pos):
            self._increment()

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_btn = 0
        if self._minus_rect().contains(pos):
            self._hovered_btn = -1
        elif self._plus_rect().contains(pos):
            self._hovered_btn = 1
        self.update()

    def leaveEvent(self, event):
        self._hovered_btn = 0
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        btn_bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
        btn_hover = QColor("#505050") if is_dark else QColor("#E0E0E0")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        accent = QColor("#0078D4")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.rect(), 8, 8)

        minus = self._minus_rect()
        painter.setBrush(btn_hover if self._hovered_btn == -1 else btn_bg)
        painter.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.addRoundedRect(minus, 8, 8)
        clip_path = QPainterPath()
        clip_path.addRect(self.rect())
        path = path & clip_path
        painter.drawPath(path)

        minus_icon = FIF.REMOVE.icon()
        painter.drawPixmap(int(minus.x() + 8), int(minus.y() + 8), minus_icon.pixmap(20, 20))

        plus = self._plus_rect()
        painter.setBrush(btn_hover if self._hovered_btn == 1 else btn_bg)
        path2 = QPainterPath()
        path2.addRoundedRect(plus, 8, 8)
        path2 = path2 & clip_path
        painter.drawPath(path2)

        plus_icon = FIF.ADD.icon()
        painter.drawPixmap(int(plus.x() + 8), int(plus.y() + 8), plus_icon.pixmap(20, 20))

        val_rect = self._value_rect()
        painter.setPen(text_color)
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)

        offset = self._scroll_offset
        if abs(offset) > 0.01:
            prev_y = val_rect.y() - offset * val_rect.height()
            curr_y = val_rect.y() + (1 - offset) * val_rect.height() if offset > 0 else val_rect.y() - (1 + offset) * val_rect.height()

            painter.save()
            clip = QPainterPath()
            clip.addRect(val_rect)
            painter.setClipPath(clip)
            painter.drawText(QRectF(val_rect.x(), prev_y, val_rect.width(), val_rect.height()),
                           Qt.AlignmentFlag.AlignCenter, str(self._prev_value))
            painter.drawText(QRectF(val_rect.x(), curr_y, val_rect.width(), val_rect.height()),
                           Qt.AlignmentFlag.AlignCenter, str(self._value))
            painter.restore()
        else:
            painter.drawText(val_rect, Qt.AlignmentFlag.AlignCenter, str(self._value))

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
