from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class OrgChartNode(QFrame):
    def __init__(self, name="", role="", parent=None):
        super().__init__(parent)
        self._name = name
        self._role = role
        self._expand_progress = 0.0

        self.setFixedSize(140, 64)
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

    def animate_in(self):
        self._expand_progress = 0.0
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def refresh_theme(self):
        self.update()

    def _is_dark(self):
        return isDarkTheme()

    def _get_initials(self):
        parts = self._name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        elif parts:
            return parts[0][0].upper()
        return ""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self._is_dark()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border_color = QColor("#444444") if dark else QColor("#DDDDDD")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#666666")
        accent = QColor("#0078D4")

        progress = self._expand_progress
        card_rect = QRectF(2, 2, 136, 60)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(card_rect, 10, 10)

        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(card_rect, 10, 10)

        if progress > 0:
            highlight = QColor(accent)
            highlight.setAlpha(int(30 * progress))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(highlight)
            painter.drawRoundedRect(card_rect, 10, 10)

        avatar_cx = 24
        avatar_cy = 32
        avatar_r = 14
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(accent)
        painter.drawEllipse(QRectF(avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_r * 2, avatar_r * 2))

        initials = self._get_initials()
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(
            QRectF(avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_r * 2, avatar_r * 2),
            Qt.AlignmentFlag.AlignCenter, initials
        )

        font.setPointSize(9)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        name_rect = QRectF(46, 14, 88, 20)
        painter.drawText(name_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._name)

        font.setPointSize(8)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(sub_color)
        role_rect = QRectF(46, 34, 88, 18)
        painter.drawText(role_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._role)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        self.animate_in()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.stop()
        super().hideEvent(event)
