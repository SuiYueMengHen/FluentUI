from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ChartZoomControl(QWidget):
    zoomChanged = Signal(int)

    def __init__(self, zoom_level=100, parent=None):
        super().__init__(parent)
        self._zoom_level = zoom_level
        self._btn_scale_in = 1.0
        self._btn_scale_out = 1.0
        self._btn_scale_reset = 1.0
        self._pressed_btn = None
        self._anim_in = QPropertyAnimation(self, b"btnScaleIn")
        self._anim_in.setDuration(150)
        self._anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_out = QPropertyAnimation(self, b"btnScaleOut")
        self._anim_out.setDuration(150)
        self._anim_out.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_reset = QPropertyAnimation(self, b"btnScaleReset")
        self._anim_reset.setDuration(150)
        self._anim_reset.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(160, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _is_dark(self):
        return isDarkTheme()

    def get_btn_scale_in(self):
        return self._btn_scale_in

    def set_btn_scale_in(self, val):
        self._btn_scale_in = val
        self.update()

    btnScaleIn = Property(float, get_btn_scale_in, set_btn_scale_in)

    def get_btn_scale_out(self):
        return self._btn_scale_out

    def set_btn_scale_out(self, val):
        self._btn_scale_out = val
        self.update()

    btnScaleOut = Property(float, get_btn_scale_out, set_btn_scale_out)

    def get_btn_scale_reset(self):
        return self._btn_scale_reset

    def set_btn_scale_reset(self, val):
        self._btn_scale_reset = val
        self.update()

    btnScaleReset = Property(float, get_btn_scale_reset, set_btn_scale_reset)

    def _btn_rects(self):
        btn_size = 36
        margin = 4
        spacing = 4
        y = (self.height() - btn_size) / 2

        zoom_out_rect = QRectF(margin, y, btn_size, btn_size)
        label_w = 56
        label_rect = QRectF(margin + btn_size + spacing, y, label_w, btn_size)
        zoom_in_rect = QRectF(margin + btn_size + spacing + label_w + spacing, y, btn_size, btn_size)
        reset_rect = QRectF(margin + btn_size * 2 + spacing * 2 + label_w + spacing, y, btn_size, btn_size)

        return zoom_out_rect, label_rect, zoom_in_rect, reset_rect

    def set_zoom_level(self, level):
        self._zoom_level = max(10, min(500, level))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        bg = QColor("#FFFFFF") if not is_dark else QColor("#2D2D2D")
        border = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")
        text_color = QColor("#1A1A1A") if not is_dark else QColor("#FFFFFF")
        dim_color = QColor("#616161") if not is_dark else QColor("#9E9E9E")
        hover_border = QColor("#0078D4")

        zoom_out_rect, label_rect, zoom_in_rect, reset_rect = self._btn_rects()

        for rect, scale, icon in [
            (zoom_out_rect, self._btn_scale_out, FIF.ZOOM_OUT),
            (zoom_in_rect, self._btn_scale_in, FIF.ZOOM_IN),
            (reset_rect, self._btn_scale_reset, FIF.FIT_PAGE),
        ]:
            cx = rect.center().x()
            cy = rect.center().y()
            sw = rect.width() * scale
            sh = rect.height() * scale
            scaled = QRectF(cx - sw / 2, cy - sh / 2, sw, sh)

            painter.setPen(QPen(border, 1))
            painter.setBrush(bg)
            painter.drawRoundedRect(scaled, 8, 8)

            icon_pixmap = icon.icon().pixmap(18, 18)
            icon_x = int(scaled.center().x() - 9)
            icon_y = int(scaled.center().y() - 9)
            painter.drawPixmap(icon_x, icon_y, icon_pixmap)

        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(label_rect, 6, 6)

        font = painter.font()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(text_color)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, f"{self._zoom_level}%")
        font.setBold(False)
        painter.setFont(font)

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            zoom_out_rect, label_rect, zoom_in_rect, reset_rect = self._btn_rects()

            if zoom_out_rect.contains(pos):
                self._pressed_btn = "out"
                self._anim_out.setStartValue(1.0)
                self._anim_out.setEndValue(0.88)
                self._anim_out.start()
            elif zoom_in_rect.contains(pos):
                self._pressed_btn = "in"
                self._anim_in.setStartValue(1.0)
                self._anim_in.setEndValue(0.88)
                self._anim_in.start()
            elif reset_rect.contains(pos):
                self._pressed_btn = "reset"
                self._anim_reset.setStartValue(1.0)
                self._anim_reset.setEndValue(0.88)
                self._anim_reset.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._pressed_btn == "out":
                self._anim_out.setStartValue(self._btn_scale_out)
                self._anim_out.setEndValue(1.0)
                self._anim_out.start()
                self._zoom_level = max(10, self._zoom_level - 10)
                self.zoomChanged.emit(self._zoom_level)
            elif self._pressed_btn == "in":
                self._anim_in.setStartValue(self._btn_scale_in)
                self._anim_in.setEndValue(1.0)
                self._anim_in.start()
                self._zoom_level = min(500, self._zoom_level + 10)
                self.zoomChanged.emit(self._zoom_level)
            elif self._pressed_btn == "reset":
                self._anim_reset.setStartValue(self._btn_scale_reset)
                self._anim_reset.setEndValue(1.0)
                self._anim_reset.start()
                self._zoom_level = 100
                self.zoomChanged.emit(self._zoom_level)
            self._pressed_btn = None
        super().mouseReleaseEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
