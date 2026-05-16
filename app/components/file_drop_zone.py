from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QLinearGradient
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class FileDropZone(QWidget):
    filesDropped = Signal(list)

    def __init__(self, label="Drop files here", parent=None):
        super().__init__(parent)
        self._label = label
        self._pulse_progress = 0.0
        self._drag_over = False
        self.setFixedSize(280, 180)
        self.setAcceptDrops(True)

        self._pulse_anim = QPropertyAnimation(self, b"pulseProgress")
        self._pulse_anim.setDuration(200)
        self._pulse_anim.setStartValue(0.0)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_pulse_progress(self):
        return self._pulse_progress

    def set_pulse_progress(self, val):
        self._pulse_progress = val
        self.update()

    pulseProgress = Property(float, get_pulse_progress, set_pulse_progress)

    def _is_dark(self):
        return isDarkTheme()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self._drag_over = True
            event.acceptProposedAction()
            self._pulse_anim.setStartValue(0.0)
            self._pulse_anim.setEndValue(1.0)
            self._pulse_anim.start()

    def dragLeaveEvent(self, event):
        self._drag_over = False
        self._pulse_anim.setStartValue(self._pulse_progress)
        self._pulse_anim.setEndValue(0.0)
        self._pulse_anim.start()

    def dropEvent(self, event):
        self._drag_over = False
        self._pulse_anim.setStartValue(self._pulse_progress)
        self._pulse_anim.setEndValue(0.0)
        self._pulse_anim.start()
        urls = event.mimeData().urls()
        files = [url.toLocalFile() for url in urls if url.isLocalFile()]
        if files:
            self.filesDropped.emit(files)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if is_dark else QColor("#888888")
        accent = QColor("#0078D4")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 12, 12)

        margin = 8
        border_rect = QRectF(margin, margin, self.width() - margin * 2, self.height() - margin * 2)

        pulse = self._pulse_progress
        if self._drag_over:
            border_pen_color = QColor(accent)
            border_pen_color.setAlphaF(0.5 + 0.5 * pulse)
            pen_width = 2.0 + pulse * 1.0
        else:
            border_pen_color = QColor(border_color)
            pen_width = 1.5

        dash_len = 8
        gap_len = 4
        pen = QPen(border_pen_color, pen_width, Qt.PenStyle.DashLine)
        pen.setDashPattern([dash_len, gap_len])
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(border_rect, 8, 8)

        cx = self.width() / 2
        cy = self.height() / 2 - 16

        icon = FIF.FOLDER_ADD.icon()
        icon_size = 36
        if self._drag_over:
            scale = 1.0 + pulse * 0.1
            painter.save()
            painter.translate(cx, cy)
            painter.scale(scale, scale)
            painter.translate(-cx, -cy)
        painter.drawPixmap(int(cx - icon_size / 2), int(cy - icon_size / 2), icon.pixmap(icon_size, icon_size))
        if self._drag_over:
            painter.restore()

        painter.setPen(accent if self._drag_over else text_color)
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(0, cy + 28, self.width(), 24),
                       Qt.AlignmentFlag.AlignCenter, self._label)

        painter.setPen(sub_color)
        font.setPointSize(9)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(QRectF(0, cy + 52, self.width(), 20),
                       Qt.AlignmentFlag.AlignCenter, "or click to browse")

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
