from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPixmap


class AvatarRing(QWidget):
    def __init__(self, avatar_path=None, size=64, ring_color1="#0078D4",
                 ring_color2="#60CDFF", ring_width=3, parent=None):
        super().__init__(parent)
        self._size = size
        self._ring_color1 = ring_color1
        self._ring_color2 = ring_color2
        self._ring_width = ring_width
        self._avatar_path = avatar_path
        self._show_status = False
        self._status_color = QColor("#6CCB5F")

        self.setFixedSize(size + ring_width * 2, size + ring_width * 2)

    def set_avatar(self, path: str):
        self._avatar_path = path
        self.update()

    def set_ring_colors(self, color1: str, color2: str):
        self._ring_color1 = color1
        self._ring_color2 = color2
        self.update()

    def set_status(self, show: bool, color="#6CCB5F"):
        self._show_status = show
        self._status_color = QColor(color)
        self.update()

    def _is_dark(self):
        from qfluentwidgets import isDarkTheme
        return isDarkTheme()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        center_x = self.width() / 2
        center_y = self.height() / 2
        outer_r = self._size / 2 + self._ring_width
        inner_r = self._size / 2

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(self._ring_color1))
        gradient.setColorAt(1, QColor(self._ring_color2))

        pen = QPen()
        pen.setWidth(self._ring_width)
        pen.setBrush(gradient)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(center_x - outer_r, center_y - outer_r, outer_r * 2, outer_r * 2))

        painter.setPen(Qt.PenStyle.NoPen)
        avatar_bg = QColor("#3D3D3D") if is_dark else QColor("#E0E0E0")
        painter.setBrush(avatar_bg)
        painter.drawEllipse(QRectF(center_x - inner_r, center_y - inner_r, inner_r * 2, inner_r * 2))

        if self._avatar_path:
            pixmap = QPixmap(self._avatar_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    int(inner_r * 2), int(inner_r * 2),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                clip_path_rect = QRectF(center_x - inner_r, center_y - inner_r, inner_r * 2, inner_r * 2)
                painter.save()
                painter.setClipRect(clip_path_rect)
                x = center_x - scaled.width() / 2
                y = center_y - scaled.height() / 2
                painter.drawPixmap(int(x), int(y), scaled)
                painter.restore()
        else:
            placeholder_color = QColor("#9E9E9E") if is_dark else QColor("#757575")
            painter.setPen(placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                QRectF(center_x - inner_r, center_y - inner_r, inner_r * 2, inner_r * 2),
                Qt.AlignmentFlag.AlignCenter, "U"
            )

        if self._show_status:
            status_r = self._size * 0.15
            status_x = center_x + inner_r * 0.65
            status_y = center_y + inner_r * 0.65

            painter.setPen(Qt.PenStyle.NoPen)
            outline_color = QColor("#202020") if is_dark else QColor("#FFFFFF")
            painter.setBrush(outline_color)
            painter.drawEllipse(QRectF(status_x - status_r - 2, status_y - status_r - 2, (status_r + 2) * 2, (status_r + 2) * 2))

            painter.setBrush(self._status_color)
            painter.drawEllipse(QRectF(status_x - status_r, status_y - status_r, status_r * 2, status_r * 2))

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
