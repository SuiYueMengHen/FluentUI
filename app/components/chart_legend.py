from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from qfluentwidgets import isDarkTheme


class ChartLegend(QWidget):
    itemToggled = Signal(int, bool)

    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._items = items or []
        self._visible = [True] * len(self._items)
        self._hovered_index = -1
        self._scale = [1.0] * len(self._items)
        self._anim_index = -1
        self._anim_scale = 1.0
        self._active_anims = []
        self.setMinimumHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _is_dark(self):
        return isDarkTheme()

    def get_anim_scale(self):
        return self._anim_scale

    def set_anim_scale(self, val):
        self._anim_scale = val
        if 0 <= self._anim_index < len(self._scale):
            self._scale[self._anim_index] = val
            self.update()

    animScale = Property(float, get_anim_scale, set_anim_scale)

    def set_items(self, items):
        self._items = list(items)
        self._visible = [True] * len(self._items)
        self._scale = [1.0] * len(self._items)
        self.update()

    def _item_rect(self, index):
        item_h = 36
        spacing = 16
        item_w = 120
        cols = max(1, self.width() // (item_w + spacing))
        col = index % cols
        row = index // cols
        x = col * (item_w + spacing)
        y = row * (item_h + 4)
        return QRectF(x, y, item_w, item_h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        text_color = QColor("#1A1A1A") if not is_dark else QColor("#FFFFFF")
        dim_color = QColor("#9E9E9E") if not is_dark else QColor("#616161")

        for i, item in enumerate(self._items):
            rect = self._item_rect(i)
            scale = self._scale[i] if i < len(self._scale) else 1.0
            cx = rect.center().x()
            cy = rect.center().y()
            scaled_w = rect.width() * scale
            scaled_h = rect.height() * scale
            scaled_rect = QRectF(cx - scaled_w / 2, cy - scaled_h / 2, scaled_w, scaled_h)

            color = QColor(item.get("color", "#0078D4"))
            square_size = 12
            square_x = scaled_rect.x() + 4
            square_y = scaled_rect.center().y() - square_size / 2
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(QRectF(square_x, square_y, square_size, square_size), 2, 2)

            font = painter.font()
            font.setPointSize(12)
            painter.setFont(font)

            visible = self._visible[i] if i < len(self._visible) else True
            if visible:
                painter.setPen(text_color)
            else:
                painter.setPen(dim_color)

            text_x = square_x + square_size + 8
            text_rect = QRectF(text_x, scaled_rect.y(), scaled_rect.width() - square_size - 12, scaled_rect.height())
            name = item.get("name", "")
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, name)

            if not visible:
                line_y = scaled_rect.center().y()
                painter.setPen(QPen(dim_color, 1))
                painter.drawLine(int(text_x), int(line_y), int(text_x + scaled_rect.width() * 0.6), int(line_y))

        painter.end()

    def _start_anim(self, index, start, end):
        self._anim_index = index
        anim = QPropertyAnimation(self, b"animScale")
        anim.setParent(self)
        anim.setDuration(150)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.finished.connect(lambda: self._cleanup_anim(anim))
        anim.start()
        self._active_anims.append(anim)

    def _cleanup_anim(self, anim):
        if anim in self._active_anims:
            self._active_anims.remove(anim)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for i in range(len(self._items)):
                if self._item_rect(i).contains(pos):
                    self._visible[i] = not self._visible[i]
                    self._start_anim(i, 1.0, 0.92)
                    self.itemToggled.emit(i, self._visible[i])
                    break
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._anim_index >= 0:
            self._start_anim(self._anim_index, self._scale[self._anim_index], 1.0)
        super().mouseReleaseEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
