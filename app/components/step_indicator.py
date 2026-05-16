from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class StepIndicator(QWidget):
    def __init__(self, steps=None, current=0, parent=None):
        super().__init__(parent)
        self._steps = steps or []
        self._current = current
        self._transition_progress = 1.0
        self._prev_current = current
        self.setFixedHeight(60)
        self._anim = QPropertyAnimation(self, b"transitionProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_transition_progress(self):
        return self._transition_progress

    def set_transition_progress(self, val):
        self._transition_progress = val
        self.update()

    transitionProgress = Property(float, get_transition_progress, set_transition_progress)

    def set_current(self, step):
        self._prev_current = self._current
        self._current = max(0, min(step, len(self._steps) - 1)) if self._steps else 0
        self._transition_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def paintEvent(self, event):
        if not self._steps:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#666666")
        accent = QColor("#0078D4")
        green = QColor("#0F7B0F")
        line_bg = QColor("#404040") if dark else QColor("#D0D0D0")
        circle_r = 14
        spacing = self.width() / max(len(self._steps), 1)
        for i, step in enumerate(self._steps):
            cx = spacing * i + spacing / 2
            cy = self.height() / 2 - 5
            if i < len(self._steps) - 1:
                line_x1 = cx + circle_r + 4
                line_x2 = spacing * (i + 1) + spacing / 2 - circle_r - 4
                pen = QPen(line_bg, 2)
                painter.setPen(pen)
                painter.drawLine(int(line_x1), int(cy), int(line_x2), int(cy))
                if i < self._current:
                    pen = QPen(green, 2)
                    painter.setPen(pen)
                    painter.drawLine(int(line_x1), int(cy), int(line_x2), int(cy))
            painter.setPen(Qt.PenStyle.NoPen)
            if i < self._current:
                painter.setBrush(green)
                painter.drawEllipse(QRectF(cx - circle_r, cy - circle_r, circle_r * 2, circle_r * 2))
                check_pen = QPen(QColor("#FFFFFF"), 2)
                painter.setPen(check_pen)
                path = QPainterPath()
                path.moveTo(cx - 5, cy)
                path.lineTo(cx - 1, cy + 4)
                path.lineTo(cx + 6, cy - 4)
                painter.drawPath(path)
            elif i == self._current:
                painter.setBrush(accent)
                painter.drawEllipse(QRectF(cx - circle_r, cy - circle_r, circle_r * 2, circle_r * 2))
                painter.setPen(QColor("#FFFFFF"))
                font = QFont()
                font.setBold(True)
                font.setPointSize(10)
                painter.setFont(font)
                painter.drawText(QRectF(cx - circle_r, cy - circle_r, circle_r * 2, circle_r * 2), Qt.AlignmentFlag.AlignCenter, str(i + 1))
            else:
                painter.setBrush(Qt.BrushStyle.NoBrush)
                pen = QPen(line_bg, 2)
                painter.setPen(pen)
                painter.drawEllipse(QRectF(cx - circle_r, cy - circle_r, circle_r * 2, circle_r * 2))
                painter.setPen(sub_color)
                font = QFont()
                font.setPointSize(10)
                painter.setFont(font)
                painter.drawText(QRectF(cx - circle_r, cy - circle_r, circle_r * 2, circle_r * 2), Qt.AlignmentFlag.AlignCenter, str(i + 1))
            painter.setPen(text_color if i <= self._current else sub_color)
            font = QFont()
            font.setPointSize(8)
            painter.setFont(font)
            label_rect = QRectF(cx - spacing / 2 + 4, cy + circle_r + 4, spacing - 8, 16)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, step)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
