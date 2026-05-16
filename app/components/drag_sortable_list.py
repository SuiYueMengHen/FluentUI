from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QMimeData
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QDrag, QPixmap
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class DragSortableList(QWidget):
    orderChanged = Signal(list)

    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._items = list(items or [])
        self._slide_offset = 0.0
        self._hovered_index = -1
        self._drag_index = -1
        self._drop_index = -1
        self._item_height = 36
        self.setFixedWidth(260)
        self._update_height()
        self.setMouseTracking(True)
        self._anim = QPropertyAnimation(self, b"slideOffset")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_slide_offset(self):
        return self._slide_offset

    def set_slide_offset(self, val):
        self._slide_offset = val
        self.update()

    slideOffset = Property(float, get_slide_offset, set_slide_offset)

    def _update_height(self):
        self.setFixedHeight(len(self._items) * self._item_height + 4)

    def set_items(self, items):
        self._items = list(items)
        self._update_height()
        self.update()

    def mouseMoveEvent(self, event):
        y = event.position().y()
        idx = int((y - 2) / self._item_height)
        if 0 <= idx < len(self._items):
            self._hovered_index = idx
        else:
            self._hovered_index = -1
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            y = event.position().y()
            idx = int((y - 2) / self._item_height)
            if 0 <= idx < len(self._items):
                handle_x = 8
                if event.position().x() <= 30:
                    self._drag_index = idx

    def mouseReleaseEvent(self, event):
        if self._drag_index >= 0 and self._drop_index >= 0 and self._drag_index != self._drop_index:
            item = self._items.pop(self._drag_index)
            self._items.insert(self._drop_index, item)
            self._update_height()
            self.orderChanged.emit(list(self._items))
            self._slide_offset = 0.0
            self._anim.stop()
            self._anim.setStartValue(10.0)
            self._anim.setEndValue(0.0)
            self._anim.start()
        self._drag_index = -1
        self._drop_index = -1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        item_bg = QColor("#353535") if dark else QColor("#F8F8F8")
        hover_bg = QColor("#3D3D3D") if dark else QColor("#EFEFEF")
        drag_bg = QColor("#0078D4")
        drag_bg.setAlpha(40)
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#888888")
        border = QColor("#505050") if dark else QColor("#E0E0E0")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
        for i, item_text in enumerate(self._items):
            y = 2 + i * self._item_height
            rect = QRectF(4, y, self.width() - 8, self._item_height - 2)
            if i == self._drag_index:
                painter.setBrush(drag_bg)
            elif i == self._hovered_index:
                painter.setBrush(hover_bg)
            else:
                painter.setBrush(item_bg)
            painter.drawRoundedRect(rect, 4, 4)
            FIF.MOVE.icon().paint(painter, QRectF(10, y + 8, 20, 20).toRect())
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(QRectF(36, y, self.width() - 44, self._item_height - 2), Qt.AlignmentFlag.AlignVCenter, item_text)
        if self._drop_index >= 0 and self._drop_index < len(self._items):
            drop_y = 2 + self._drop_index * self._item_height
            pen = QPen(QColor("#0078D4"), 2)
            painter.setPen(pen)
            painter.drawLine(4, int(drop_y), self.width() - 4, int(drop_y))
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
