from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme, IconWidget


class FlowchartNode(QFrame):
    def __init__(self, title="", subtitle="", node_type="process", parent=None):
        super().__init__(parent)
        self._title = title
        self._subtitle = subtitle
        self._node_type = node_type
        self._draw_progress = 0.0
        self._icon = None

        self.setFixedSize(160, 80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"drawProgress")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        if node_type == "start":
            self._icon = FIF.PLAY
        elif node_type == "end":
            self._icon = FIF.CLOSE
        elif node_type == "decision":
            self._icon = FIF.QUESTION

    def get_draw_progress(self):
        return self._draw_progress

    def set_draw_progress(self, val):
        self._draw_progress = val
        self.update()

    drawProgress = Property(float, get_draw_progress, set_draw_progress)

    def animate_in(self):
        self._draw_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
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
        border_color = QColor("#555555") if dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#666666")

        progress = self._draw_progress

        if self._node_type == "start":
            self._draw_start(painter, bg, border_color, text_color, sub_color, progress)
        elif self._node_type == "process":
            self._draw_process(painter, bg, border_color, text_color, sub_color, progress)
        elif self._node_type == "decision":
            self._draw_decision(painter, bg, border_color, text_color, sub_color, progress)
        elif self._node_type == "end":
            self._draw_end(painter, bg, border_color, text_color, sub_color, progress)
        else:
            self._draw_process(painter, bg, border_color, text_color, sub_color, progress)

        painter.end()

    def _draw_start(self, painter, bg, border, text, sub, progress):
        rect = QRectF(4, 4, 152, 72)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 20, 20)

        pen = QPen(border)
        pen.setWidth(2)
        pen.setDashPattern([1.0, 0.0])
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        self._draw_partial_path(painter, path, pen, progress)

        self._draw_text(painter, text, sub, rect)

    def _draw_process(self, painter, bg, border, text, sub, progress):
        rect = QRectF(4, 4, 152, 72)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 8, 8)

        pen = QPen(border)
        pen.setWidth(2)
        path = QPainterPath()
        path.addRoundedRect(rect, 8, 8)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        self._draw_partial_path(painter, path, pen, progress)

        self._draw_text(painter, text, sub, rect)

    def _draw_decision(self, painter, bg, border, text, sub, progress):
        cx, cy = 80, 40
        dx, dy = 72, 34
        diamond = QPainterPath()
        diamond.moveTo(cx, cy - dy)
        diamond.lineTo(cx + dx, cy)
        diamond.lineTo(cx, cy + dy)
        diamond.lineTo(cx - dx, cy)
        diamond.closeSubpath()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawPath(diamond)

        pen = QPen(border)
        pen.setWidth(2)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        self._draw_partial_path(painter, diamond, pen, progress)

        text_rect = QRectF(cx - 40, cy - 14, 80, 28)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._title)

    def _draw_end(self, painter, bg, border, text, sub, progress):
        rect = QRectF(4, 4, 152, 72)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 20, 20)

        pen = QPen(border)
        pen.setWidth(2)
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        self._draw_partial_path(painter, path, pen, progress)

        inner = rect.adjusted(6, 6, -6, -6)
        pen2 = QPen(border)
        pen2.setWidth(2)
        path2 = QPainterPath()
        path2.addRoundedRect(inner, 14, 14)
        self._draw_partial_path(painter, path2, pen2, progress)

        self._draw_text(painter, text, sub, rect)

    def _draw_partial_path(self, painter, path, pen, progress):
        if progress <= 0:
            return
        total = path.length()
        if total <= 0:
            return
        draw_len = total * progress
        visible_dash = draw_len
        invisible_dash = total - draw_len
        if invisible_dash <= 0:
            pen.setDashPattern([1.0, 0.0])
        else:
            pen.setDashPattern([visible_dash, invisible_dash])
        pen.setDashOffset(0)
        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_text(self, painter, text_color, sub_color, rect):
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        if self._subtitle:
            title_rect = QRectF(rect.x(), rect.y() + 12, rect.width(), 24)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, self._title)
            font.setPointSize(8)
            font.setBold(False)
            painter.setFont(font)
            painter.setPen(sub_color)
            sub_rect = QRectF(rect.x(), rect.y() + 36, rect.width(), 20)
            painter.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, self._subtitle)
        else:
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self._title)

    def showEvent(self, event):
        super().showEvent(event)
        self.animate_in()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()
        super().hideEvent(event)
