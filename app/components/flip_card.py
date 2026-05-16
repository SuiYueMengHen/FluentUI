from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen


class FlipCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._flip_progress = 0.0
        self._is_flipped = False
        self._front_widget = None
        self._back_widget = None

        self.setFixedSize(200, 160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._flip_anim = QPropertyAnimation(self, b"flipProgress")
        self._flip_anim.setDuration(500)
        self._flip_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def _is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def get_flip_progress(self):
        return self._flip_progress

    def set_flip_progress(self, val):
        self._flip_progress = val
        self.update()

    flipProgress = Property(float, get_flip_progress, set_flip_progress)

    def set_front(self, widget):
        if self._front_widget:
            self._front_widget.deleteLater()
        self._front_widget = widget
        widget.setParent(self)
        widget.hide()
        self.update()

    def set_back(self, widget):
        if self._back_widget:
            self._back_widget.deleteLater()
        self._back_widget = widget
        widget.setParent(self)
        widget.hide()
        self.update()

    def flip(self):
        self._is_flipped = not self._is_flipped
        self._flip_anim.setStartValue(0.0)
        self._flip_anim.setEndValue(1.0)
        self._flip_anim.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.flip()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg_color = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor(255, 255, 255, 20) if is_dark else QColor(0, 0, 0, 25)

        w = self.width()
        h = self.height()
        border_r = 12

        if self._flip_progress < 0.5:
            scale_x = 1.0 - self._flip_progress * 2
        else:
            scale_x = (self._flip_progress - 0.5) * 2

        scaled_w = w * max(scale_x, 0.01)
        x_offset = (w - scaled_w) / 2

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(bg_color)
        painter.drawRoundedRect(QRectF(x_offset, 0, scaled_w, h), border_r, border_r)

        if scale_x > 0.05:
            current_widget = self._back_widget if self._flip_progress >= 0.5 else self._front_widget
            if current_widget:
                current_widget.setGeometry(
                    int(x_offset), 0,
                    int(scaled_w), h
                )
                if not current_widget.isVisible():
                    other = self._back_widget if self._flip_progress < 0.5 else self._front_widget
                    if other:
                        other.hide()
                    current_widget.show()

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
