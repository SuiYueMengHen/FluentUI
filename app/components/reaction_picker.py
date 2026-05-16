from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class ReactionPicker(QWidget):
    reactionSelected = Signal(str)

    REACTIONS = ["like", "love", "laugh", "wow", "sad", "angry"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected = ""
        self._hover_index = -1
        self._pop_progress = 0.0
        self._anim = QPropertyAnimation(self, b"popProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(6 * 40 + 8, 48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def get_pop_progress(self):
        return self._pop_progress

    def set_pop_progress(self, val):
        self._pop_progress = val
        self.update()

    popProgress = Property(float, get_pop_progress, set_pop_progress)

    def _reaction_at(self, x):
        idx = int((x - 4) / 40)
        if 0 <= idx < 6:
            return idx
        return -1

    def mouseMoveEvent(self, event):
        self._hover_index = self._reaction_at(event.position().x())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hover_index = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            idx = self._reaction_at(event.position().x())
            if 0 <= idx < 6:
                self._selected = self.REACTIONS[idx]
                self.reactionSelected.emit(self._selected)
        super().mousePressEvent(event)

    def _draw_reaction(self, painter, cx, cy, r, reaction, is_hover):
        is_dark = isDarkTheme()
        if is_hover:
            bg = QColor("#0078D4")
        else:
            bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))
        border_color = QColor("#555555") if is_dark else QColor("#E0E0E0")
        if is_hover:
            border_color = QColor("#0078D4")
        painter.setPen(QPen(border_color, 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))
        face_color = QColor("#FFFFFF") if is_hover else (QColor("#D4D4D4") if is_dark else QColor("#616161"))
        painter.setPen(QPen(face_color, 1.5))
        eye_y = cy - r * 0.2
        eye_r = r * 0.08
        painter.drawEllipse(QRectF(cx - r * 0.3 - eye_r, eye_y - eye_r, eye_r * 2, eye_r * 2))
        painter.drawEllipse(QRectF(cx + r * 0.3 - eye_r, eye_y - eye_r, eye_r * 2, eye_r * 2))
        mouth_y = cy + r * 0.2
        mouth_w = r * 0.35
        if reaction == "like":
            painter.drawArc(int(cx - mouth_w), int(mouth_y - r * 0.12), int(mouth_w * 2), int(r * 0.35), 0, -180 * 16)
        elif reaction == "love":
            heart_path = QPainterPath()
            s = r * 0.25
            hx = cx
            hy = cy + r * 0.15
            heart_path.moveTo(hx, hy + s * 0.3)
            heart_path.cubicTo(hx, hy - s * 0.3, hx - s, hy - s * 0.3, hx - s, hy + s * 0.1)
            heart_path.cubicTo(hx - s, hy + s * 0.6, hx, hy + s * 0.9, hx, hy + s)
            heart_path.cubicTo(hx, hy + s * 0.9, hx + s, hy + s * 0.6, hx + s, hy + s * 0.1)
            heart_path.cubicTo(hx + s, hy - s * 0.3, hx, hy - s * 0.3, hx, hy + s * 0.3)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#FF4444") if is_hover else (QColor("#FF6666") if not is_dark else QColor("#CC4444")))
            painter.drawPath(heart_path)
        elif reaction == "laugh":
            painter.drawArc(int(cx - mouth_w), int(mouth_y - r * 0.15), int(mouth_w * 2), int(r * 0.45), 0, -180 * 16)
            painter.drawLine(int(cx - r * 0.35), int(eye_y + r * 0.1), int(cx - r * 0.15), int(eye_y + r * 0.15))
            painter.drawLine(int(cx + r * 0.35), int(eye_y + r * 0.1), int(cx + r * 0.15), int(eye_y + r * 0.15))
        elif reaction == "wow":
            painter.setPen(QPen(face_color, 1.5))
            painter.drawEllipse(QRectF(cx - r * 0.12, int(mouth_y - r * 0.05), r * 0.24, r * 0.24))
        elif reaction == "sad":
            painter.drawArc(int(cx - mouth_w), int(mouth_y + r * 0.05), int(mouth_w * 2), int(r * 0.3), 0, 180 * 16)
        elif reaction == "angry":
            painter.drawArc(int(cx - mouth_w), int(mouth_y + r * 0.05), int(mouth_w * 2), int(r * 0.3), 0, 180 * 16)
            brow_y = eye_y - r * 0.18
            painter.drawLine(int(cx - r * 0.45), int(brow_y - r * 0.08), int(cx - r * 0.15), int(brow_y + r * 0.05))
            painter.drawLine(int(cx + r * 0.45), int(brow_y - r * 0.08), int(cx + r * 0.15), int(brow_y + r * 0.05))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border = QColor("#555555") if is_dark else QColor("#E0E0E0")
        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 24, 24)
        scale = self._pop_progress
        for i, reaction in enumerate(self.REACTIONS):
            cx = 4 + i * 40 + 20
            cy = 24
            r = 14 * scale
            is_hover = (i == self._hover_index)
            if is_hover:
                r = 16
            self._draw_reaction(painter, cx, cy, r, reaction, is_hover)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
