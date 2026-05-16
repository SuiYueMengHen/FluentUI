from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient
from qfluentwidgets import isDarkTheme


class RangeSlider(QWidget):
    rangeChanged = Signal(int, int)

    def __init__(self, min_val=0, max_val=100, low=20, high=80, parent=None):
        super().__init__(parent)
        self._min_val = min_val
        self._max_val = max_val
        self._low = low
        self._high = high
        self._dragging = None
        self._handle_size = 20
        self._track_h = 6
        self._low_anim_pos = 0.0
        self._high_anim_pos = 0.0
        self._anim_low = QPropertyAnimation(self, b"lowAnimPos")
        self._anim_low.setDuration(150)
        self._anim_low.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_high = QPropertyAnimation(self, b"highAnimPos")
        self._anim_high.setDuration(150)
        self._anim_high.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedHeight(44)
        self.setMinimumWidth(200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._sync_anim_pos()

    def _is_dark(self):
        return isDarkTheme()

    def _sync_anim_pos(self):
        self._low_anim_pos = self._val_to_pos(self._low)
        self._high_anim_pos = self._val_to_pos(self._high)

    def _val_to_pos(self, val):
        if self._max_val == self._min_val:
            return 0.0
        margin = self._handle_size / 2 + 4
        track_w = self.width() - margin * 2
        return margin + (val - self._min_val) / (self._max_val - self._min_val) * track_w

    def _pos_to_val(self, pos):
        margin = self._handle_size / 2 + 4
        track_w = self.width() - margin * 2
        if track_w <= 0:
            return self._min_val
        ratio = (pos - margin) / track_w
        ratio = max(0.0, min(1.0, ratio))
        return int(self._min_val + ratio * (self._max_val - self._min_val))

    def get_low_anim_pos(self):
        return self._low_anim_pos

    def set_low_anim_pos(self, val):
        self._low_anim_pos = val
        self.update()

    lowAnimPos = Property(float, get_low_anim_pos, set_low_anim_pos)

    def get_high_anim_pos(self):
        return self._high_anim_pos

    def set_high_anim_pos(self, val):
        self._high_anim_pos = val
        self.update()

    highAnimPos = Property(float, get_high_anim_pos, set_high_anim_pos)

    def set_range(self, min_val, max_val):
        self._min_val = min_val
        self._max_val = max_val
        self._low = max(self._low, min_val)
        self._high = min(self._high, max_val)
        self._sync_anim_pos()
        self.update()

    def set_values(self, low, high, animate=True):
        self._low = max(self._min_val, min(low, self._max_val))
        self._high = max(self._min_val, min(high, self._max_val))
        if self._low > self._high:
            self._low, self._high = self._high, self._low
        if animate:
            self._anim_low.setStartValue(self._low_anim_pos)
            self._anim_low.setEndValue(self._val_to_pos(self._low))
            self._anim_low.start()
            self._anim_high.setStartValue(self._high_anim_pos)
            self._anim_high.setEndValue(self._val_to_pos(self._high))
            self._anim_high.start()
        else:
            self._sync_anim_pos()
            self.update()
        self.rangeChanged.emit(self._low, self._high)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        track_color = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")
        fill_color = QColor("#0078D4")
        handle_color = QColor("#FFFFFF") if not is_dark else QColor("#E0E0E0")
        handle_border = QColor("#0078D4")
        handle_shadow = QColor(0, 0, 0, 30) if not is_dark else QColor(0, 0, 0, 60)

        cy = self.height() / 2
        margin = self._handle_size / 2 + 4
        track_w = self.width() - margin * 2

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        track_rect = QRectF(margin, cy - self._track_h / 2, track_w, self._track_h)
        painter.drawRoundedRect(track_rect, 3, 3)

        fill_x = self._low_anim_pos
        fill_w = self._high_anim_pos - self._low_anim_pos
        if fill_w > 0:
            fill_rect = QRectF(fill_x, cy - self._track_h / 2, fill_w, self._track_h)
            painter.setBrush(fill_color)
            painter.drawRoundedRect(fill_rect, 3, 3)

        for pos in [self._low_anim_pos, self._high_anim_pos]:
            hx = pos - self._handle_size / 2
            hy = cy - self._handle_size / 2
            shadow_rect = QRectF(hx + 1, hy + 1, self._handle_size, self._handle_size)
            painter.setBrush(handle_shadow)
            painter.drawEllipse(shadow_rect)

            handle_rect = QRectF(hx, hy, self._handle_size, self._handle_size)
            painter.setPen(QPen(handle_border, 2))
            painter.setBrush(handle_color)
            painter.drawEllipse(handle_rect)

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            low_dist = abs(x - self._low_anim_pos)
            high_dist = abs(x - self._high_anim_pos)
            if low_dist <= high_dist:
                self._dragging = "low"
            else:
                self._dragging = "high"
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            val = self._pos_to_val(event.position().x())
            if self._dragging == "low":
                self._low = min(val, self._high)
            else:
                self._high = max(val, self._low)
            self._sync_anim_pos()
            self.update()
            self.rangeChanged.emit(self._low, self._high)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._dragging:
            self._dragging = None
            self._anim_low.setStartValue(self._low_anim_pos)
            self._anim_low.setEndValue(self._val_to_pos(self._low))
            self._anim_low.start()
            self._anim_high.setStartValue(self._high_anim_pos)
            self._anim_high.setEndValue(self._val_to_pos(self._high))
            self._anim_high.start()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_anim_pos()

    def refresh_theme(self):
        self.update()
        self.repaint()
