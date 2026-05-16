from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ChartExportMenu(QWidget):
    exportRequested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._formats = ["PNG", "SVG", "CSV", "PDF"]
        self._menu_open = False
        self._menu_progress = 0.0
        self._hovered_format = -1
        self._anim = QPropertyAnimation(self, b"menuProgress")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._collapse_timer = QTimer(self)
        self._collapse_timer.setSingleShot(True)
        self._collapse_timer.setInterval(150)
        self._collapse_timer.timeout.connect(self._collapse_menu)
        self.setFixedSize(120, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _is_dark(self):
        return isDarkTheme()

    def get_menu_progress(self):
        return self._menu_progress

    def set_menu_progress(self, val):
        self._menu_progress = val
        self.update()

    menuProgress = Property(float, get_menu_progress, set_menu_progress)

    def _button_rect(self):
        return QRectF(0, 0, self.width(), 44)

    def _menu_item_rect(self, index):
        item_h = 36
        return QRectF(0, 44 + index * item_h, self.width(), item_h)

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

        save_pixmap = FIF.SAVE.icon().pixmap(16, 16)
        painter.drawPixmap(int(10), int(14), save_pixmap)

        font = painter.font()
        font.setPointSize(11)
        painter.setFont(font)
        painter.setPen(text_color)
        text_rect = QRectF(30, 0, btn.width() - 50, 44)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, "Export")

        down_pixmap = FIF.DOWN.icon().pixmap(12, 12)
        painter.drawPixmap(int(btn.width() - 24), int(16), down_pixmap)

        if self._menu_progress > 0:
            menu_h = len(self._formats) * 36 * self._menu_progress
            menu_rect = QRectF(0, 44, self.width(), menu_h)
            painter.setPen(QPen(border, 1))
            painter.setBrush(bg)
            painter.drawRoundedRect(menu_rect, 8, 8)

            visible = int(len(self._formats) * self._menu_progress)
            for i in range(visible):
                item_rect = self._menu_item_rect(i)
                if i == self._hovered_format:
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(hover_bg)
                    painter.drawRoundedRect(item_rect.adjusted(2, 1, -2, -1), 4, 4)

                painter.setPen(text_color if i != self._hovered_format else accent)
                font.setBold(i == self._hovered_format)
                painter.setFont(font)
                painter.drawText(item_rect.adjusted(12, 0, -12, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._formats[i])
                font.setBold(False)
                painter.setFont(font)

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if self._button_rect().contains(pos):
                self._menu_open = not self._menu_open
                if self._menu_open:
                    self._anim.setStartValue(0.0)
                    self._anim.setEndValue(1.0)
                    self.setFixedHeight(44 + len(self._formats) * 36)
                else:
                    self._anim.setStartValue(self._menu_progress)
                    self._anim.setEndValue(0.0)
                    self._collapse_timer.start()
                self._anim.start()
            elif self._menu_open:
                for i in range(len(self._formats)):
                    if self._menu_item_rect(i).contains(pos):
                        self.exportRequested.emit(self._formats[i])
                        self._menu_open = False
                        self._anim.setStartValue(self._menu_progress)
                        self._anim.setEndValue(0.0)
                        self._anim.start()
                        self._collapse_timer.start()
                        break
        super().mousePressEvent(event)

    def _collapse_menu(self):
        if not self._menu_open:
            self.setFixedHeight(44)

    def mouseMoveEvent(self, event):
        if self._menu_open:
            pos = event.position()
            self._hovered_format = -1
            for i in range(len(self._formats)):
                if self._menu_item_rect(i).contains(pos):
                    self._hovered_format = i
                    break
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_format = -1
        self.update()
        super().leaveEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
