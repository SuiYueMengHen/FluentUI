from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ImageGallery(QWidget):
    def __init__(self, images=None, columns=3, parent=None):
        super().__init__(parent)
        self._images = images or []
        self._columns = columns
        self._fade_progress = 0.0
        self._hovered_index = -1
        self._cell_spacing = 8
        self._cell_height = 140
        self.setMinimumSize(300, 200)
        self.setMouseTracking(True)

        self._fade_anim = QPropertyAnimation(self, b"fadeProgress")
        self._fade_anim.setDuration(200)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._first_show = True

    def get_fade_progress(self):
        return self._fade_progress

    def set_fade_progress(self, val):
        self._fade_progress = val
        self.update()

    fadeProgress = Property(float, get_fade_progress, set_fade_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _get_cell_rects(self):
        rects = []
        if not self._images:
            return rects
        w = self.width()
        col_w = (w - self._cell_spacing * (self._columns + 1)) / self._columns
        for i, img in enumerate(self._images):
            row = i // self._columns
            col = i % self._columns
            x = self._cell_spacing + col * (col_w + self._cell_spacing)
            y = self._cell_spacing + row * (self._cell_height + self._cell_spacing)
            rects.append(QRectF(x, y, col_w, self._cell_height))
        return rects

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_index = -1
        for i, rect in enumerate(self._get_cell_rects()):
            if rect.contains(pos):
                self._hovered_index = i
                break
        self.update()

    def leaveEvent(self, event):
        self._hovered_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#1E1E1E") if is_dark else QColor("#F5F5F5")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        overlay_color = QColor(0, 0, 0, int(120 * self._fade_progress))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRect(self.rect())

        cell_rects = self._get_cell_rects()
        for i, rect in enumerate(cell_rects):
            img = self._images[i]
            color = QColor(img.get("color", "#0078D4"))
            alpha_color = QColor(color)
            alpha_color.setAlphaF(self._fade_progress)
            painter.setBrush(alpha_color)
            painter.drawRoundedRect(rect, 8, 8)

            if i == self._hovered_index:
                painter.setBrush(overlay_color)
                painter.drawRoundedRect(rect, 8, 8)
                title = img.get("title", "")
                painter.setPen(text_color)
                font = painter.font()
                font.setPointSize(11)
                painter.setFont(font)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, title)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self._fade_anim.start()

    def hideEvent(self, event):
        if self._fade_anim.state() == QPropertyAnimation.State.Running:
            self._fade_anim.pause()
        super().hideEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
