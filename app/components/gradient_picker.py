from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class GradientPicker(QWidget):
    gradientChanged = Signal(str, str)

    def __init__(self, color1="#0078D4", color2="#005A9E", parent=None):
        super().__init__(parent)
        self._color1 = QColor(color1)
        self._color2 = QColor(color2)
        self._stop1_pos = 0.0
        self._stop2_pos = 1.0
        self._anim_progress = 0.0
        self._dragging_stop = 0
        self.setFixedSize(240, 100)
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

    def _gradient_bar_rect(self):
        return QRectF(10, 10, 220, 40)

    def _stop1_handle_rect(self):
        bar = self._gradient_bar_rect()
        x = bar.x() + self._stop1_pos * bar.width()
        return QRectF(x - 7, bar.bottom() + 4, 14, 20)

    def _stop2_handle_rect(self):
        bar = self._gradient_bar_rect()
        x = bar.x() + self._stop2_pos * bar.width()
        return QRectF(x - 7, bar.bottom() + 4, 14, 20)

    def _preview_rect(self):
        return QRectF(10, 78, 220, 14)

    def mousePressEvent(self, event):
        pos = event.position()
        if self._stop1_handle_rect().adjusted(-4, -4, 4, 4).contains(pos):
            self._dragging_stop = 1
        elif self._stop2_handle_rect().adjusted(-4, -4, 4, 4).contains(pos):
            self._dragging_stop = 2

    def mouseMoveEvent(self, event):
        if self._dragging_stop == 0:
            return
        bar = self._gradient_bar_rect()
        ratio = max(0.0, min(1.0, (event.position().x() - bar.x()) / bar.width()))
        if self._dragging_stop == 1:
            self._stop1_pos = min(ratio, self._stop2_pos - 0.05)
        elif self._dragging_stop == 2:
            self._stop2_pos = max(ratio, self._stop1_pos + 0.05)
        self.gradientChanged.emit(self._color1.name(), self._color2.name())
        self.update()

    def mouseReleaseEvent(self, event):
        self._dragging_stop = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        handle_bg = QColor("#3D3D3D") if is_dark else QColor("#E0E0E0")

        bar = self._gradient_bar_rect()
        grad = QLinearGradient(bar.topLeft(), bar.topRight())
        grad.setColorAt(self._stop1_pos, self._color1)
        grad.setColorAt(self._stop2_pos, self._color2)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(grad)
        painter.drawRoundedRect(bar, 6, 6)

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(bar, 6, 6)

        for stop_idx, (handle_rect, color) in enumerate([
            (self._stop1_handle_rect(), self._color1),
            (self._stop2_handle_rect(), self._color2),
        ]):
            path = QPainterPath()
            x = handle_rect.center().x()
            top_y = handle_rect.top()
            path.moveTo(x, top_y - 4)
            path.lineTo(x - 7, top_y + 6)
            path.lineTo(x + 7, top_y + 6)
            path.closeSubpath()
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)

            painter.setPen(QPen(border_color, 1))
            painter.setBrush(handle_bg)
            painter.drawRoundedRect(QRectF(handle_rect.x(), top_y + 6, handle_rect.width(), handle_rect.height() - 6), 3, 3)

            painter.setPen(text_color)
            font = painter.font()
            font.setPointSize(7)
            painter.setFont(font)
            painter.drawText(QRectF(handle_rect.x(), top_y + 6, handle_rect.width(), handle_rect.height() - 6),
                           Qt.AlignmentFlag.AlignCenter, str(stop_idx + 1))

        pr = self._preview_rect()
        preview_grad = QLinearGradient(pr.topLeft(), pr.topRight())
        preview_grad.setColorAt(self._stop1_pos, self._color1)
        preview_grad.setColorAt(self._stop2_pos, self._color2)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(preview_grad)
        painter.drawRoundedRect(pr, 4, 4)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
