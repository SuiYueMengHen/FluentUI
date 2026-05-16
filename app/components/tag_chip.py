from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class TagChip(QWidget):
    removed = Signal()
    selectedChanged = Signal(bool)

    def __init__(self, text="", color="#0078D4", removable=True, selected=False, parent=None):
        super().__init__(parent)
        self._text = text
        self._color = color
        self._removable = removable
        self._selected = selected
        self._scale_anim = 1.0
        self._hover = False
        self._hover_close = False
        self._anim = QPropertyAnimation(self, b"scaleAnim")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedHeight(28)
        self._update_width()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def _update_width(self):
        from PySide6.QtGui import QFontMetrics
        font = QFont()
        font.setPixelSize(12)
        fm = QFontMetrics(font)
        tw = fm.horizontalAdvance(self._text)
        w = tw + 32 + (20 if self._removable else 0)
        self.setFixedWidth(max(60, w))

    def get_scale_anim(self):
        return self._scale_anim

    def set_scale_anim(self, val):
        self._scale_anim = val
        self.update()

    scaleAnim = Property(float, get_scale_anim, set_scale_anim)

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self._update_width()
        self.update()

    def is_selected(self):
        return self._selected

    def set_selected(self, selected):
        if selected != self._selected:
            self._selected = selected
            self._anim.setStartValue(1.0)
            self._anim.setKeyValueAt(0.4, 1.05)
            self._anim.setEndValue(1.0)
            self._anim.start()
            self.selectedChanged.emit(selected)
        self.update()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._hover_close = False
        self.update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        if self._removable:
            close_x = self.width() - 20
            pos = event.position()
            self._hover_close = pos.x() >= close_x and pos.x() <= self.width()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if self._removable and pos.x() >= self.width() - 20:
                self.removed.emit()
                return
            self.set_selected(not self._selected)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        painter.save()
        cx = self.width() / 2
        cy = self.height() / 2
        painter.translate(cx, cy)
        painter.scale(self._scale_anim, self._scale_anim)
        painter.translate(-cx, -cy)
        rect = QRectF(0, 0, self.width(), self.height())
        radius = 14
        if self._selected:
            bg = QColor(self._color)
            bg.setAlpha(40)
            border = QColor(self._color)
        elif self._hover:
            bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
            border = QColor("#555555") if is_dark else QColor("#CCCCCC")
        else:
            bg = QColor("#2D2D2D") if is_dark else QColor("#FAFAFA")
            border = QColor("#555555") if is_dark else QColor("#E0E0E0")
        painter.setPen(QPen(border, 1.5))
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, radius, radius)
        dot_r = 4
        dot_x = 12
        dot_y = self.height() / 2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self._color))
        painter.drawEllipse(QRectF(dot_x - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2))
        text_color = QColor("#D4D4D4") if is_dark else QColor("#1A1A1A")
        if self._selected:
            text_color = QColor(self._color)
        painter.setPen(text_color)
        font = QFont()
        font.setPixelSize(12)
        painter.setFont(font)
        text_x = 22
        text_w = self.width() - 32 - (20 if self._removable else 0)
        painter.drawText(QRectF(text_x, 0, text_w, self.height()), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text)
        if self._removable:
            close_x = self.width() - 16
            close_y = self.height() / 2
            close_color = QColor("#9E9E9E") if is_dark else QColor("#757575")
            if self._hover_close:
                close_color = QColor("#FF4444")
            painter.setPen(QPen(close_color, 1.5))
            painter.drawLine(int(close_x - 4), int(close_y - 4), int(close_x + 4), int(close_y + 4))
            painter.drawLine(int(close_x + 4), int(close_y - 4), int(close_x - 4), int(close_y + 4))
        painter.restore()
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
