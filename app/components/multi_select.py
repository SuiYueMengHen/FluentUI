from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class MultiSelect(QWidget):
    selectionChanged = Signal(list)

    def __init__(self, options=None, parent=None):
        super().__init__(parent)
        self._options = options or []
        self._expanded = False
        self._expand_progress = 0.0
        self._hovered_index = -1
        self._hovered_trigger = False
        self.setFixedWidth(240)
        self.setFixedHeight(36)
        self.setMouseTracking(True)

        self._expand_anim = QPropertyAnimation(self, b"expandProgress")
        self._expand_anim.setDuration(200)
        self._expand_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._expand_anim.valueChanged.connect(self._on_expand_changed)

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress(self, val):
        self._expand_progress = val
        self.update()

    expandProgress = Property(float, get_expand_progress, set_expand_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _on_expand_changed(self, val):
        item_h = 32
        total_h = 36 + len(self._options) * item_h * self._expand_progress
        self.setFixedHeight(int(total_h))

    def _trigger_rect(self):
        return QRectF(0, 0, self.width(), 36)

    def _item_rect(self, index):
        item_h = 32
        return QRectF(0, 36 + index * item_h, self.width(), item_h)

    def _selected_count(self):
        return sum(1 for o in self._options if o.get("selected", False))

    def _toggle_expand(self):
        self._expanded = not self._expanded
        if self._expanded:
            self._expand_anim.setStartValue(0.0)
            self._expand_anim.setEndValue(1.0)
        else:
            self._expand_anim.setStartValue(1.0)
            self._expand_anim.setEndValue(0.0)
        self._expand_anim.start()

    def mousePressEvent(self, event):
        pos = event.position()
        if self._trigger_rect().contains(pos):
            self._toggle_expand()
            return
        if self._expanded:
            for i in range(len(self._options)):
                if self._item_rect(i).contains(pos):
                    self._options[i]["selected"] = not self._options[i].get("selected", False)
                    self.selectionChanged.emit([o for o in self._options if o.get("selected", False)])
                    self.update()
                    break

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_trigger = self._trigger_rect().contains(pos)
        self._hovered_index = -1
        if self._expanded:
            for i in range(len(self._options)):
                if self._item_rect(i).contains(pos):
                    self._hovered_index = i
                    break
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if is_dark else QColor("#666666")
        hover_bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
        accent = QColor("#0078D4")
        check_color = QColor("#FFFFFF")

        trigger = self._trigger_rect()
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(trigger, 6, 6)

        count = self._selected_count()
        label = f"{count} selected" if count > 0 else "Select options..."
        painter.setPen(text_color if count > 0 else sub_color)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(QRectF(10, 0, trigger.width() - 30, 36),
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)

        arrow = FIF.DOWN.icon()
        painter.drawPixmap(int(trigger.right() - 24), 8, arrow.pixmap(20, 20))

        if self._expand_progress > 0:
            painter.setOpacity(self._expand_progress)
            for i, option in enumerate(self._options):
                rect = self._item_rect(i)
                if i == self._hovered_index:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(hover_bg)
                    painter.drawRect(rect)

                selected = option.get("selected", False)
                check_rect = QRectF(rect.x() + 10, rect.center().y() - 8, 16, 16)
                painter.setPen(QPen(accent if selected else border_color, 1.5))
                painter.setBrush(accent if selected else Qt.BrushStyle.NoBrush)
                painter.drawRoundedRect(check_rect, 3, 3)

                if selected:
                    painter.setPen(QPen(check_color, 2))
                    cx = check_rect.center().x()
                    cy = check_rect.center().y()
                    painter.drawLine(int(cx - 4), int(cy), int(cx - 1), int(cy + 3))
                    painter.drawLine(int(cx - 1), int(cy + 3), int(cx + 4), int(cy - 3))

                painter.setPen(text_color)
                font.setPointSize(10)
                painter.setFont(font)
                painter.drawText(QRectF(rect.x() + 34, rect.y(), rect.width() - 44, rect.height()),
                               Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, option.get("text", ""))

            painter.setOpacity(1.0)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
