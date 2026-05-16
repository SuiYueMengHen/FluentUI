from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ColorPicker(QWidget):
    colorChanged = Signal(str)

    def __init__(self, color="#0078D4", parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._hue = self._color.hueF()
        self._saturation = self._color.saturationF()
        self._brightness = self._color.valueF()
        self._anim_progress = 0.0
        self._dragging_hue = False
        self._dragging_sb = False
        self._prev_color = QColor(color)
        self.setFixedSize(220, 240)
        self.setMouseTracking(True)

        self._anim = QPropertyAnimation(self, b"animProgress")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_anim_progress(self):
        return self._anim_progress

    def set_anim_progress(self, val):
        self._anim_progress = val
        self.update()

    animProgress = Property(float, get_anim_progress, set_anim_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _sb_rect(self):
        return QRectF(10, 10, 200, 150)

    def _hue_rect(self):
        return QRectF(10, 175, 200, 16)

    def _preview_rect(self):
        return QRectF(10, 205, 200, 24)

    def _update_color_from_sb(self, x, y):
        sb = self._sb_rect()
        self._saturation = max(0.0, min(1.0, (x - sb.x()) / sb.width()))
        self._brightness = max(0.0, min(1.0, 1.0 - (y - sb.y()) / sb.height()))
        self._color = QColor.fromHsvF(self._hue, self._saturation, self._brightness)
        self.colorChanged.emit(self._color.name())
        self.update()

    def _update_hue(self, x):
        hr = self._hue_rect()
        self._hue = max(0.0, min(1.0, (x - hr.x()) / hr.width()))
        self._color = QColor.fromHsvF(self._hue, self._saturation, self._brightness)
        self.colorChanged.emit(self._color.name())
        self.update()

    def mousePressEvent(self, event):
        pos = event.position()
        if self._sb_rect().contains(pos):
            self._dragging_sb = True
            self._update_color_from_sb(pos.x(), pos.y())
        elif self._hue_rect().contains(pos):
            self._dragging_hue = True
            self._update_hue(pos.x())

    def mouseMoveEvent(self, event):
        pos = event.position()
        if self._dragging_sb:
            self._update_color_from_sb(pos.x(), pos.y())
        elif self._dragging_hue:
            self._update_hue(pos.x())

    def mouseReleaseEvent(self, event):
        self._dragging_sb = False
        self._dragging_hue = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")

        sb = self._sb_rect()
        hue_color = QColor.fromHsvF(self._hue, 1.0, 1.0)
        grad_w = QLinearGradient(sb.topLeft(), sb.topRight())
        grad_w.setColorAt(0, QColor("#FFFFFF"))
        grad_w.setColorAt(1, hue_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(grad_w)
        painter.drawRoundedRect(sb, 4, 4)

        grad_b = QLinearGradient(sb.topLeft(), sb.bottomLeft())
        grad_b.setColorAt(0, QColor(0, 0, 0, 0))
        grad_b.setColorAt(1, QColor(0, 0, 0, 255))
        painter.setBrush(grad_b)
        painter.drawRoundedRect(sb, 4, 4)

        sel_x = sb.x() + self._saturation * sb.width()
        sel_y = sb.y() + (1.0 - self._brightness) * sb.height()
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(sel_x - 6, sel_y - 6, 12, 12))

        hr = self._hue_rect()
        hue_grad = QLinearGradient(hr.topLeft(), hr.topRight())
        for i in range(11):
            hue_grad.setColorAt(i / 10.0, QColor.fromHsvF(i / 10.0, 1.0, 1.0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(hue_grad)
        painter.drawRoundedRect(hr, 8, 8)

        hue_x = hr.x() + self._hue * hr.width()
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(hue_x - 6, hr.y() + 2, 12, 12))

        pr = self._preview_rect()
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(self._color)
        painter.drawRoundedRect(pr, 4, 4)

        painter.setPen(text_color)
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        painter.drawText(pr, Qt.AlignmentFlag.AlignCenter, self._color.name().upper())

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
