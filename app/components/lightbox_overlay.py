from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class LightboxOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0.0
        self._content_widget = None
        self._close_rect = QRectF(0, 0, 32, 32)
        self.setVisible(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        self._anim = QPropertyAnimation(self, b"progress")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_progress(self):
        return self._progress

    def set_progress(self, val):
        self._progress = val
        self.update()

    progress = Property(float, get_progress, set_progress)

    def _is_dark(self):
        return isDarkTheme()

    def show_content(self, widget):
        self._content_widget = widget
        self.setVisible(True)
        self.raise_()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def close_lightbox(self):
        try:
            self._anim.finished.disconnect(self._hide_self)
        except (RuntimeError, TypeError):
            pass
        self._anim.setStartValue(self._progress)
        self._anim.setEndValue(0.0)
        self._anim.finished.connect(self._hide_self)
        self._anim.start()

    def _hide_self(self):
        self._anim.finished.disconnect(self._hide_self)
        self.setVisible(False)
        self._content_widget = None

    def mousePressEvent(self, event):
        pos = event.position()
        if self._close_rect.contains(pos):
            self.close_lightbox()
            return
        content_rect = self._content_area_rect()
        if content_rect and not content_rect.contains(pos):
            self.close_lightbox()

    def _content_area_rect(self):
        if not self._content_widget:
            return None
        w = min(600, self.width() - 80)
        h = min(400, self.height() - 80)
        x = (self.width() - w) / 2
        y = (self.height() - h) / 2
        return QRectF(x, y, w, h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()

        overlay_alpha = int(180 * self._progress)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, overlay_alpha))
        painter.drawRect(self.rect())

        content_rect = self._content_area_rect()
        if content_rect:
            scale = 0.9 + 0.1 * self._progress
            cx = content_rect.center().x()
            cy = content_rect.center().y()
            painter.translate(cx, cy)
            painter.scale(scale, scale)
            painter.translate(-cx, -cy)

            card_bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
            painter.setBrush(card_bg)
            painter.drawRoundedRect(content_rect, 12, 12)

            close_x = content_rect.right() - 40
            close_y = content_rect.top() + 8
            self._close_rect = QRectF(close_x, close_y, 32, 32)
            painter.setBrush(QColor("#3D3D3D") if is_dark else QColor("#E0E0E0"))
            painter.drawRoundedRect(self._close_rect, 6, 6)
            close_icon = FIF.CLOSE.icon()
            painter.drawPixmap(int(self._close_rect.x() + 6), int(self._close_rect.y() + 6), close_icon.pixmap(20, 20))

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
