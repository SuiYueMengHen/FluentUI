from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class InfiniteLoader(QWidget):
    loadMore = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._loaded_items = []
        self._shimmer_offset = 0.0
        self._loading = False
        self._skeleton_count = 3
        self._item_height = 40
        self.setFixedWidth(280)
        self.setMinimumHeight(200)
        self._shimmer_anim = QPropertyAnimation(self, b"shimmerOffset")
        self._shimmer_anim.setDuration(1500)
        self._shimmer_anim.setStartValue(-1.0)
        self._shimmer_anim.setEndValue(2.0)
        self._shimmer_anim.setLoopCount(-1)
        self._shimmer_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._scroll_timer = QTimer(self)
        self._scroll_timer.timeout.connect(self._check_load)

    def showEvent(self, event):
        super().showEvent(event)
        self._shimmer_anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._shimmer_anim.stop()

    def get_shimmer_offset(self):
        return self._shimmer_offset

    def set_shimmer_offset(self, val):
        self._shimmer_offset = val
        self.update()

    shimmerOffset = Property(float, get_shimmer_offset, set_shimmer_offset)

    def add_items(self, items):
        self._loaded_items.extend(items)
        self._loading = False
        self.update()

    def set_loading(self, loading):
        self._loading = loading
        if loading:
            self.loadMore.emit()

    def _check_load(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        skeleton_base = QColor("#353535") if dark else QColor("#E8E8E8")
        skeleton_hi = QColor("#454545") if dark else QColor("#F5F5F5")
        item_bg = QColor("#353535") if dark else QColor("#F8F8F8")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)
        y = 4
        for item_text in self._loaded_items:
            if y + self._item_height > self.height():
                break
            rect = QRectF(4, y, self.width() - 8, self._item_height - 4)
            painter.setBrush(item_bg)
            painter.drawRoundedRect(rect, 6, 6)
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(QRectF(14, y, self.width() - 28, self._item_height - 4), Qt.AlignmentFlag.AlignVCenter, item_text)
            y += self._item_height
        for i in range(self._skeleton_count):
            if y + self._item_height > self.height():
                break
            rect = QRectF(4, y, self.width() - 8, self._item_height - 4)
            painter.setBrush(skeleton_base)
            painter.drawRoundedRect(rect, 6, 6)
            gradient = QLinearGradient()
            offset = self._shimmer_offset
            gradient.setStart(self.width() * offset - self.width() * 0.3, 0)
            gradient.setFinalStop(self.width() * offset + self.width() * 0.3, 0)
            gradient.setColorAt(0, QColor(255, 255, 255, 0))
            gradient.setColorAt(0.5, QColor(255, 255, 255, 30))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(gradient)
            painter.drawRoundedRect(rect, 6, 6)
            y += self._item_height
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
