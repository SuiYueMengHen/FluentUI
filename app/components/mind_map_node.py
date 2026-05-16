from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme, IconWidget


class MindMapNode(QWidget):
    expandChanged = Signal(bool)

    LEVEL_COLORS = ["#0078D4", "#107C10", "#CA5010", "#8764B8", "#D13438"]

    def __init__(self, title="", level=0, parent=None):
        super().__init__(parent)
        self._title = title
        self._level = level
        self._expanded = False
        self._expand_progress = 0.0

        self.setFixedHeight(36)
        self.setMinimumWidth(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"expandProgress")
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress(self, val):
        self._expand_progress = val
        self.update()

    expandProgress = Property(float, get_expand_progress, set_expand_progress)

    def is_expanded(self):
        return self._expanded

    def set_expanded(self, expanded):
        self._expanded = expanded
        self._anim.setStartValue(self._expand_progress)
        self._anim.setEndValue(1.0 if expanded else 0.0)
        self._anim.start()
        self.expandChanged.emit(expanded)

    def refresh_theme(self):
        self.update()

    def _is_dark(self):
        return isDarkTheme()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_expanded(not self._expanded)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self._is_dark()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        border_color = QColor("#444444") if dark else QColor("#DDDDDD")

        rect = QRectF(0, 0, self.width() - 1, self.height() - 1)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 8, 8)

        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, 8, 8)

        accent_color = QColor(self.LEVEL_COLORS[self._level % len(self.LEVEL_COLORS)])
        accent_rect = QRectF(0, 4, 4, self.height() - 9)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(accent_color)
        painter.drawRoundedRect(accent_rect, 2, 2)

        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(text_color)
        text_rect = QRectF(12, 0, self.width() - 40, self.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._title)

        icon_x = self.width() - 24
        icon_y = self.height() / 2
        painter.setPen(accent_color)
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        if self._expanded:
            painter.drawText(QRectF(icon_x - 6, icon_y - 8, 16, 16), Qt.AlignmentFlag.AlignCenter, "-")
        else:
            painter.drawText(QRectF(icon_x - 6, icon_y - 8, 16, 16), Qt.AlignmentFlag.AlignCenter, "+")

        painter.end()
