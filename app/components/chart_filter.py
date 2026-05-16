from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from qfluentwidgets import isDarkTheme


class ChartFilter(QWidget):
    filterChanged = Signal(list)

    def __init__(self, filters=None, parent=None):
        super().__init__(parent)
        self._filters = filters or []
        self._chip_scales = []
        self._anim_index = -1
        self._anim = QPropertyAnimation(self, b"chipScale")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._init_scales()
        self.setFixedHeight(44)
        self.setMinimumWidth(100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _is_dark(self):
        return isDarkTheme()

    def _init_scales(self):
        self._chip_scales = [1.0] * len(self._filters)

    def get_chip_scale(self):
        if 0 <= self._anim_index < len(self._chip_scales):
            return self._chip_scales[self._anim_index]
        return 1.0

    def set_chip_scale(self, val):
        if 0 <= self._anim_index < len(self._chip_scales):
            self._chip_scales[self._anim_index] = val
            self.update()

    chipScale = Property(float, get_chip_scale, set_chip_scale)

    def set_filters(self, filters):
        self._filters = list(filters)
        self._init_scales()
        self.update()

    def _chip_rect(self, index):
        chip_h = 32
        spacing = 8
        padding = 4
        x = padding
        for i in range(index):
            name = self._filters[i].get("name", "")
            chip_w = max(80, len(name) * 9 + 36)
            x += chip_w + spacing
        name = self._filters[index].get("name", "")
        chip_w = max(80, len(name) * 9 + 36)
        y = (self.height() - chip_h) / 2
        return QRectF(x, y, chip_w, chip_h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg_active = QColor("#E3F2FD") if not is_dark else QColor("#1A3A5C")
        bg_inactive = QColor("#F5F5F5") if not is_dark else QColor("#2D2D2D")
        border_active = QColor("#0078D4")
        border_inactive = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")
        text_active = QColor("#0078D4") if not is_dark else QColor("#64B5F6")
        text_inactive = QColor("#9E9E9E") if not is_dark else QColor("#616161")

        font = painter.font()
        font.setPointSize(11)
        painter.setFont(font)

        for i, f in enumerate(self._filters):
            rect = self._chip_rect(i)
            scale = self._chip_scales[i] if i < len(self._chip_scales) else 1.0
            cx = rect.center().x()
            cy = rect.center().y()
            sw = rect.width() * scale
            sh = rect.height() * scale
            scaled = QRectF(cx - sw / 2, cy - sh / 2, sw, sh)

            active = f.get("active", True)
            if active:
                painter.setPen(QPen(border_active, 1.5))
                painter.setBrush(bg_active)
            else:
                painter.setPen(QPen(border_inactive, 1))
                painter.setBrush(bg_inactive)
            painter.drawRoundedRect(scaled, scaled.height() / 2, scaled.height() / 2)

            color = QColor(f.get("color", "#0078D4"))
            dot_r = 5
            dot_x = scaled.x() + 12
            dot_y = scaled.center().y()
            painter.setPen(Qt.PenStyle.NoPen)
            if active:
                painter.setBrush(color)
            else:
                color.setAlpha(100)
                painter.setBrush(color)
            painter.drawEllipse(QRectF(dot_x - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2))

            name = f.get("name", "")
            painter.setPen(text_active if active else text_inactive)
            text_rect = QRectF(dot_x + dot_r + 6, scaled.y(), scaled.width() - 30, scaled.height())
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, name)

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for i in range(len(self._filters)):
                if self._chip_rect(i).contains(pos):
                    self._filters[i]["active"] = not self._filters[i].get("active", True)
                    self._anim_index = i
                    self._anim.setStartValue(1.0)
                    self._anim.setEndValue(0.93)
                    self._anim.start()
                    active_names = [f["name"] for f in self._filters if f.get("active", True)]
                    self.filterChanged.emit(active_names)
                    break
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._anim_index >= 0:
            self._anim.setStartValue(self._chip_scales[self._anim_index])
            self._anim.setEndValue(1.0)
            self._anim.start()
        super().mouseReleaseEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
