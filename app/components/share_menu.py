from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ShareMenu(QWidget):
    shareRequested = Signal(str)

    OPTIONS = [
        ("Copy Link", FIF.LINK),
        ("Email", FIF.MAIL),
        ("Twitter", FIF.GLOBE),
        ("Facebook", FIF.PEOPLE),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._menu_open = False
        self._slide_progress = 0.0
        self._hover_index = -1
        self._anim = QPropertyAnimation(self, b"slideProgress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(120, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

    def get_slide_progress(self):
        return self._slide_progress

    def set_slide_progress(self, val):
        self._slide_progress = val
        self.update()
        if val > 0:
            self.setFixedHeight(int(36 + val * len(self.OPTIONS) * 36))
        else:
            self.setFixedHeight(36)

    slideProgress = Property(float, get_slide_progress, set_slide_progress)

    def toggle_menu(self):
        self._menu_open = not self._menu_open
        if self._menu_open:
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(1.0)
            self._anim.start()
        else:
            self._anim.setStartValue(self._slide_progress)
            self._anim.setEndValue(0.0)
            self._anim.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if pos.y() < 36:
                self.toggle_menu()
            else:
                idx = int((pos.y() - 36) / 36)
                if 0 <= idx < len(self.OPTIONS):
                    self.shareRequested.emit(self.OPTIONS[idx][0])
                    self.toggle_menu()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position()
        if pos.y() >= 36:
            self._hover_index = int((pos.y() - 36) / 36)
        else:
            self._hover_index = -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hover_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        btn_rect = QRectF(0, 0, self.width(), 36)
        btn_bg = QColor("#0078D4")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(btn_bg)
        painter.drawRoundedRect(btn_rect, 18, 18)
        icon = FIF.SHARE
        icon_pixmap = icon.icon().pixmap(14, 14)
        painter.drawPixmap(16, 11, icon_pixmap)
        painter.setPen(QColor("#FFFFFF"))
        font = QFont()
        font.setPixelSize(12)
        font.setWeight(QFont.Weight.Medium)
        painter.setFont(font)
        painter.drawText(btn_rect.adjusted(34, 0, 0, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "Share")
        if self._slide_progress > 0:
            menu_top = 36
            menu_height = self._slide_progress * len(self.OPTIONS) * 36
            menu_rect = QRectF(0, menu_top, self.width(), menu_height)
            menu_bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
            menu_border = QColor("#555555") if is_dark else QColor("#E0E0E0")
            painter.setPen(QPen(menu_border, 1))
            painter.setBrush(menu_bg)
            painter.drawRoundedRect(menu_rect, 8, 8)
            painter.setClipRect(menu_rect)
            for i, (label, icon_enum) in enumerate(self.OPTIONS):
                item_y = menu_top + i * 36 * self._slide_progress
                item_rect = QRectF(0, item_y, self.width(), 36 * self._slide_progress)
                if i == self._hover_index:
                    hover_bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(hover_bg)
                    painter.drawRect(item_rect)
                opt_icon_pixmap = icon_enum.icon().pixmap(14, 14)
                icon_y = item_y + (36 * self._slide_progress - 14) / 2
                painter.drawPixmap(12, int(icon_y), opt_icon_pixmap)
                text_color = QColor("#D4D4D4") if is_dark else QColor("#1A1A1A")
                painter.setPen(text_color)
                font.setPixelSize(11)
                painter.setFont(font)
                painter.drawText(item_rect.adjusted(32, 0, 0, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, label)
            painter.setClipping(False)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
