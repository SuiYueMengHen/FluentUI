from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from qfluentwidgets import isDarkTheme


class ChartAxis(QWidget):
    def __init__(self, orientation="horizontal", labels=None, parent=None):
        super().__init__(parent)
        self._orientation = orientation
        self._labels = labels or []
        self._fade_progress = 0.0
        self._anim = QPropertyAnimation(self, b"fadeProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        if self._orientation == "horizontal":
            self.setFixedHeight(36)
        else:
            self.setFixedWidth(48)

    def _is_dark(self):
        return isDarkTheme()

    def get_fade_progress(self):
        return self._fade_progress

    def set_fade_progress(self, val):
        self._fade_progress = val
        self.update()

    fadeProgress = Property(float, get_fade_progress, set_fade_progress)

    def set_labels(self, labels):
        self._labels = list(labels)
        self._fade_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def show(self):
        super().show()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._fade_progress)

        is_dark = self._is_dark()
        line_color = QColor("#BDBDBD") if not is_dark else QColor("#4A4A4A")
        label_color = QColor("#616161") if not is_dark else QColor("#9E9E9E")
        tick_color = QColor("#9E9E9E") if not is_dark else QColor("#616161")

        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)

        if self._orientation == "horizontal":
            w = self.width()
            h = self.height()
            painter.setPen(QPen(line_color, 1))
            painter.drawLine(0, 0, w, 0)

            if self._labels:
                spacing = w / max(len(self._labels), 1)
                for i, label in enumerate(self._labels):
                    x = spacing * i + spacing / 2
                    painter.setPen(QPen(tick_color, 1))
                    painter.drawLine(int(x), 0, int(x), 5)
                    painter.setPen(label_color)
                    text_rect = QRectF(spacing * i, 7, spacing, h - 7)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(label))
        else:
            w = self.width()
            h = self.height()
            painter.setPen(QPen(line_color, 1))
            painter.drawLine(w - 1, 0, w - 1, h)

            if self._labels:
                spacing = h / max(len(self._labels), 1)
                for i, label in enumerate(self._labels):
                    y = h - spacing * i - spacing / 2
                    painter.setPen(QPen(tick_color, 1))
                    painter.drawLine(w - 6, int(y), w - 1, int(y))
                    painter.setPen(label_color)
                    text_rect = QRectF(0, spacing * i, w - 8, spacing)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, str(label))

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
