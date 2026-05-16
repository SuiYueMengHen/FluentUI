from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class TimeRangePicker(QWidget):
    rangeSelected = Signal(str)

    def __init__(self, ranges=None, parent=None):
        super().__init__(parent)
        self._ranges = ranges or ["Today", "7D", "30D", "90D", "1Y", "Custom"]
        self._selected = self._ranges[0] if self._ranges else ""
        self._dropdown_open = False
        self._dropdown_progress = 0.0
        self._anim = QPropertyAnimation(self, b"dropdownProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._collapse_timer = QTimer(self)
        self._collapse_timer.setSingleShot(True)
        self._collapse_timer.setInterval(200)
        self._collapse_timer.timeout.connect(self._collapse_dropdown)
        self.setFixedHeight(44)
        self.setMinimumWidth(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _is_dark(self):
        return isDarkTheme()

    def get_dropdown_progress(self):
        return self._dropdown_progress

    def set_dropdown_progress(self, val):
        self._dropdown_progress = val
        self.update()

    dropdownProgress = Property(float, get_dropdown_progress, set_dropdown_progress)

    def set_ranges(self, ranges):
        self._ranges = list(ranges)
        self._selected = self._ranges[0] if self._ranges else ""
        self.update()

    def _button_rect(self):
        return QRectF(0, 0, self.width(), 44)

    def _dropdown_rect(self):
        item_h = 36
        padding = 4
        visible = int(len(self._ranges) * self._dropdown_progress)
        h = visible * item_h + padding * 2
        return QRectF(0, 44, self.width(), h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg = QColor("#FFFFFF") if not is_dark else QColor("#2D2D2D")
        border = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")
        text_color = QColor("#1A1A1A") if not is_dark else QColor("#FFFFFF")
        dim_color = QColor("#616161") if not is_dark else QColor("#9E9E9E")
        hover_bg = QColor("#F5F5F5") if not is_dark else QColor("#3D3D3D")
        accent = QColor("#0078D4")

        btn = self._button_rect()
        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(btn, 8, 8)

        font = painter.font()
        font.setPointSize(11)
        painter.setFont(font)
        painter.setPen(text_color)
        text_rect = QRectF(12, 0, btn.width() - 40, 44)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._selected)

        arrow_x = btn.width() - 24
        arrow_y = btn.center().y()
        arrow_size = 5
        painter.setPen(QPen(dim_color, 1.5))
        if self._dropdown_open:
            painter.drawLine(int(arrow_x - arrow_size), int(arrow_y + arrow_size / 2), int(arrow_x), int(arrow_y - arrow_size / 2))
            painter.drawLine(int(arrow_x), int(arrow_y - arrow_size / 2), int(arrow_x + arrow_size), int(arrow_y + arrow_size / 2))
        else:
            painter.drawLine(int(arrow_x - arrow_size), int(arrow_y - arrow_size / 2), int(arrow_x), int(arrow_y + arrow_size / 2))
            painter.drawLine(int(arrow_x), int(arrow_y + arrow_size / 2), int(arrow_x + arrow_size), int(arrow_y - arrow_size / 2))

        if self._dropdown_progress > 0:
            dd = self._dropdown_rect()
            painter.setPen(QPen(border, 1))
            painter.setBrush(bg)
            painter.drawRoundedRect(dd, 8, 8)

            item_h = 36
            padding = 4
            visible = int(len(self._ranges) * self._dropdown_progress)
            for i in range(visible):
                item_rect = QRectF(padding, 44 + padding + i * item_h, self.width() - padding * 2, item_h)
                if self._ranges[i] == self._selected:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(accent)
                    painter.setOpacity(0.1)
                    painter.drawRoundedRect(item_rect, 6, 6)
                    painter.setOpacity(1.0)
                    painter.setPen(accent)
                else:
                    painter.setPen(text_color)
                font.setPointSize(11)
                font.setBold(self._ranges[i] == self._selected)
                painter.setFont(font)
                painter.drawText(item_rect.adjusted(12, 0, -12, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._ranges[i])

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if self._button_rect().contains(pos):
                self._dropdown_open = not self._dropdown_open
                if self._dropdown_open:
                    self._anim.setStartValue(0.0)
                    self._anim.setEndValue(1.0)
                    self.setFixedHeight(44 + len(self._ranges) * 36 + 8)
                else:
                    self._anim.setStartValue(self._dropdown_progress)
                    self._anim.setEndValue(0.0)
                    self._collapse_timer.start()
                self._anim.start()
            elif self._dropdown_open:
                item_h = 36
                padding = 4
                for i in range(len(self._ranges)):
                    item_rect = QRectF(padding, 44 + padding + i * item_h, self.width() - padding * 2, item_h)
                    if item_rect.contains(pos):
                        self._selected = self._ranges[i]
                        self.rangeSelected.emit(self._selected)
                        self._dropdown_open = False
                        self._anim.setStartValue(self._dropdown_progress)
                        self._anim.setEndValue(0.0)
                        self._anim.start()
                        self._collapse_timer.start()
                        break
        super().mousePressEvent(event)

    def _collapse_dropdown(self):
        if not self._dropdown_open:
            self.setFixedHeight(44)

    def refresh_theme(self):
        self.update()
        self.repaint()
