from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush


class ShimmerWidget(QWidget):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"

    def __init__(self, width=200, height=20, shape="rectangle", parent=None):
        super().__init__(parent)
        self._shape = shape
        self._shimmer_offset = 0.0
        self.setFixedSize(width, height)

        self._anim = QPropertyAnimation(self, b"shimmerOffset")
        self._anim.setDuration(1500)
        self._anim.setStartValue(-1.0)
        self._anim.setEndValue(2.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self._anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._anim.stop()

    def get_shimmer_offset(self):
        return self._shimmer_offset

    def set_shimmer_offset(self, val):
        self._shimmer_offset = val
        self.update()

    shimmerOffset = Property(float, get_shimmer_offset, set_shimmer_offset)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self.is_dark()
        base_color = QColor("#2D2D2D") if is_dark else QColor("#E8E8E8")
        highlight_color = QColor("#3D3D3D") if is_dark else QColor("#F5F5F5")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(base_color)

        if self._shape == self.CIRCLE:
            r = min(self.width(), self.height()) / 2
            painter.drawEllipse(QRectF(0, 0, r * 2, r * 2))
        else:
            painter.drawRoundedRect(self.rect(), 6, 6)

        gradient = QLinearGradient()
        offset = self._shimmer_offset
        gradient.setStart(self.width() * offset - self.width() * 0.3, 0)
        gradient.setFinalStop(self.width() * offset + self.width() * 0.3, 0)
        gradient.setColorAt(0, QColor(255, 255, 255, 0))
        gradient.setColorAt(0.5, QColor(255, 255, 255, 40))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))

        painter.setBrush(gradient)
        if self._shape == self.CIRCLE:
            painter.drawEllipse(QRectF(0, 0, r * 2, r * 2))
        else:
            painter.drawRoundedRect(self.rect(), 6, 6)

        painter.end()

    def is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def refresh_theme(self):
        self.update()
        self.repaint()
