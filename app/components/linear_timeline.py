from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class LinearTimeline(QWidget):
    def __init__(self, events=None, parent=None):
        super().__init__(parent)
        self._events = events or []
        self._draw_progress = 0.0
        self.setFixedHeight(70)
        self._anim = QPropertyAnimation(self, b"drawProgress")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_draw_progress(self):
        return self._draw_progress

    def set_draw_progress(self, val):
        self._draw_progress = val
        self.update()

    drawProgress = Property(float, get_draw_progress, set_draw_progress)

    def paintEvent(self, event):
        if not self._events:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        line_color = QColor("#404040") if dark else QColor("#D0D0D0")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#666666")
        n = len(self._events)
        spacing = self.width() / max(n, 1)
        line_y = 30
        pen = QPen(line_color, 2)
        painter.setPen(pen)
        progress_width = (self.width() - spacing) * self._draw_progress
        painter.drawLine(int(spacing / 2), line_y, int(spacing / 2 + progress_width), line_y)
        remaining_start = int(spacing / 2 + progress_width)
        if remaining_start < self.width() - int(spacing / 2):
            painter.drawLine(remaining_start, line_y, self.width() - int(spacing / 2), line_y)
        for i, evt in enumerate(self._events):
            cx = spacing * i + spacing / 2
            dot_r = 6
            color = QColor(evt.get("color", "#0078D4"))
            x_ratio = cx / self.width()
            if x_ratio <= self._draw_progress:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(QRectF(cx - dot_r, line_y - dot_r, dot_r * 2, dot_r * 2))
                painter.setPen(QColor("#FFFFFF"))
                font = QFont()
                font.setPointSize(6)
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(QRectF(cx - dot_r, line_y - dot_r, dot_r * 2, dot_r * 2), Qt.AlignmentFlag.AlignCenter, str(i + 1))
            else:
                painter.setPen(QPen(line_color, 2))
                painter.setBrush(QColor("#2D2D2D") if dark else QColor("#FFFFFF"))
                painter.drawEllipse(QRectF(cx - dot_r, line_y - dot_r, dot_r * 2, dot_r * 2))
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(8)
            font.setBold(True)
            painter.setFont(font)
            title_rect = QRectF(cx - spacing / 2 + 4, line_y + 10, spacing - 8, 14)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, evt.get("title", ""))
            painter.setPen(sub_color)
            font.setPointSize(7)
            font.setBold(False)
            painter.setFont(font)
            time_rect = QRectF(cx - spacing / 2 + 4, line_y - 20, spacing - 8, 14)
            painter.drawText(time_rect, Qt.AlignmentFlag.AlignCenter, evt.get("time", ""))
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
