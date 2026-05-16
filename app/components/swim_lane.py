from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class SwimLane(QWidget):
    def __init__(self, title="", color="#0078D4", parent=None):
        super().__init__(parent)
        self._title = title
        self._color = color
        self._expand_progress = 1.0
        self._collapsed = False

        self.setMinimumWidth(220)
        self.setMinimumHeight(200)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 44, 0, 0)
        self._layout.setSpacing(8)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self._anim = QPropertyAnimation(self, b"expandProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress(self, val):
        self._expand_progress = val
        self.update()
        self.setFixedHeight(int(44 + (self.minimumHeight() - 44) * val) if val < 1.0 else self.minimumHeight())

    expandProgress = Property(float, get_expand_progress, set_expand_progress)

    def add_card(self, widget):
        self._layout.addWidget(widget)

    def toggle_collapse(self):
        self._collapsed = not self._collapsed
        self._anim.setStartValue(self._expand_progress)
        self._anim.setEndValue(0.0 if self._collapsed else 1.0)
        self._anim.start()

    def refresh_theme(self):
        self.update()

    def _is_dark(self):
        return isDarkTheme()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self._is_dark()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        header_bg = QColor(self._color)
        text_color = QColor("#FFFFFF")
        border_color = QColor("#444444") if dark else QColor("#DDDDDD")
        body_bg = QColor("#252525") if dark else QColor("#FAFAFA")

        lane_rect = QRectF(0, 0, self.width(), self.height())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(lane_rect, 10, 10)

        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(lane_rect, 10, 10)

        header_rect = QRectF(0, 0, self.width(), 40)
        header_path = QPainterPath()
        header_path.addRoundedRect(lane_rect, 10, 10)
        clip_bottom = QPainterPath()
        clip_bottom.addRect(QRectF(0, 0, self.width(), 40))
        painter.setClipPath(header_path.intersected(clip_bottom))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(header_bg)
        painter.drawRect(QRectF(0, 0, self.width(), 40))
        painter.setClipping(False)

        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        title_rect = QRectF(12, 0, self.width() - 24, 40)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._title)

        if self._expand_progress > 0:
            body_rect = QRectF(1, 41, self.width() - 2, self.height() - 42)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(body_bg)
            painter.drawRect(body_rect)

        painter.end()
