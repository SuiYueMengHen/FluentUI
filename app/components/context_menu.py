from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ContextMenu(QWidget):
    itemSelected = Signal(str)

    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._items = []
        if items:
            for item in items:
                if isinstance(item, str):
                    self._items.append({"text": item})
                else:
                    self._items.append(item)
        self._scale_progress = 1.0
        self._hovered_index = -1
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self._anim = QPropertyAnimation(self, b"scaleProgress")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_scale_progress(self):
        return self._scale_progress

    def set_scale_progress(self, val):
        self._scale_progress = val
        self.update()

    scaleProgress = Property(float, get_scale_progress, set_scale_progress)

    def _calc_size(self):
        w = 200
        h = 4
        for item in self._items:
            if item.get("separator"):
                h += 9
            else:
                h += 32
        h += 4
        return w, h

    def popup(self, pos):
        w, h = self._calc_size()
        self.setFixedSize(w, h)
        self.move(pos)
        self._scale_progress = 0.95
        self._anim.stop()
        self._anim.setStartValue(0.95)
        self._anim.setEndValue(1.0)
        self._anim.start()
        self.show()

    def mouseMoveEvent(self, event):
        y = event.position().y()
        item_y = 4
        self._hovered_index = -1
        for i, item in enumerate(self._items):
            if item.get("separator"):
                item_y += 9
            else:
                if item_y <= y <= item_y + 32:
                    self._hovered_index = i
                item_y += 32
        self.update()

    def mousePressEvent(self, event):
        if self._hovered_index >= 0 and self._hovered_index < len(self._items):
            item = self._items[self._hovered_index]
            if not item.get("separator"):
                self.itemSelected.emit(item.get("text", ""))
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border = QColor("#505050") if dark else QColor("#D0D0D0")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        hover_bg = QColor("#3D3D3D") if dark else QColor("#F0F0F0")
        sep_color = QColor("#505050") if dark else QColor("#E0E0E0")
        cx = self.width() / 2
        cy = self.height() / 2
        painter.save()
        painter.translate(cx, cy)
        painter.scale(self._scale_progress, self._scale_progress)
        painter.translate(-cx, -cy)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
        pen = QPen(border, 1)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
        item_y = 4
        for i, item in enumerate(self._items):
            if item.get("separator"):
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(sep_color)
                painter.drawRect(QRectF(12, item_y + 4, self.width() - 24, 1))
                item_y += 9
            else:
                if i == self._hovered_index:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(hover_bg)
                    painter.drawRoundedRect(QRectF(4, item_y, self.width() - 8, 32), 4, 4)
                icon = item.get("icon")
                if icon is not None:
                    icon.icon().paint(painter, QRectF(12, item_y + 6, 20, 20).toRect())
                painter.setPen(text_color)
                font = QFont()
                font.setPointSize(10)
                painter.setFont(font)
                text_x = 40 if icon is not None else 16
                painter.drawText(QRectF(text_x, item_y, self.width() - text_x - 8, 32), Qt.AlignmentFlag.AlignVCenter, item.get("text", ""))
                item_y += 32
        painter.restore()
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
