from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, IconWidget, isDarkTheme

TOAST_TYPES = {
    "info": {"color": "#0078D4", "icon": FIF.INFO},
    "success": {"color": "#0F7B0F", "icon": FIF.COMPLETED},
    "warning": {"color": "#9D5D00", "icon": FIF.RINGER},
    "error": {"color": "#C42B1C", "icon": FIF.CLOSE},
}


class _CloseButton(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 44)
        self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        icon_size = 12
        icon_x = (self.width() - icon_size) / 2
        icon_y = (self.height() - icon_size) / 2

        if self._hovered:
            hover_color = QColor(255, 255, 255, 20) if dark else QColor(0, 0, 0, 20)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(hover_color)
            painter.drawRoundedRect(QRectF(self.rect()), 6, 6)

        FIF.CLOSE.icon().paint(painter, QRectF(icon_x, icon_y, icon_size, icon_size).toRect())
        painter.end()


class Toast(QFrame):
    dismissed = Signal()

    def __init__(self, message="", toast_type="info", parent=None):
        super().__init__(parent)
        self._message = message
        self._toast_type = toast_type if toast_type in TOAST_TYPES else "info"
        self._slide_offset = 1.0
        self._opacity = 1.0

        self.setFixedHeight(48)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._h_layout = QHBoxLayout(self)
        self._h_layout.setContentsMargins(16, 0, 8, 0)
        self._h_layout.setSpacing(8)

        type_cfg = TOAST_TYPES[self._toast_type]

        self._icon_widget = IconWidget(type_cfg["icon"], self)
        self._icon_widget.setFixedSize(24, 24)
        self._h_layout.addWidget(self._icon_widget)

        self._label = QLabel(self._message, self)
        self._label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._h_layout.addWidget(self._label)

        self._h_layout.addStretch()

        self._close_btn = _CloseButton(self)
        self._close_btn.clicked.connect(self.dismiss)
        self._h_layout.addWidget(self._close_btn)

        self._slide_anim = QPropertyAnimation(self, b"slideOffset")
        self._slide_anim.setDuration(200)
        self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._fade_anim = QPropertyAnimation(self, b"opacity")
        self._fade_anim.setDuration(200)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._fade_anim.finished.connect(self._on_fade_finished)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(4000)
        self._timer.timeout.connect(self.dismiss)

        self.refresh_theme()

    def get_slide_offset(self):
        return self._slide_offset

    def set_slide_offset(self, val):
        self._slide_offset = val
        self.move(self.x(), int(-self.height() * self._slide_offset))
        self.update()

    slideOffset = Property(float, get_slide_offset, set_slide_offset)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, val):
        self._opacity = val
        self.update()

    opacity = Property(float, get_opacity, set_opacity)

    def show_toast(self):
        self.show()
        self._slide_anim.setStartValue(1.0)
        self._slide_anim.setEndValue(0.0)
        self._slide_anim.start()
        self._timer.start()

    def dismiss(self):
        if self._fade_anim.state() == QPropertyAnimation.State.Running:
            return
        self._timer.stop()
        self._fade_anim.setStartValue(self._opacity)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.start()

    def _on_fade_finished(self):
        self.hide()
        self.dismissed.emit()
        self.deleteLater()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity)

        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border = QColor(255, 255, 255, 20) if dark else QColor(0, 0, 0, 25)
        accent = QColor(TOAST_TYPES[self._toast_type]["color"])

        rect = QRectF(self.rect())

        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 8, 8)

        painter.save()
        clip_path = QPainterPath()
        clip_path.addRoundedRect(rect, 8, 8)
        painter.setClipPath(clip_path)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(accent)
        painter.drawRect(QRectF(0, 0, 4, self.height()))
        painter.restore()

        painter.end()

    def refresh_theme(self):
        dark = isDarkTheme()
        text_color = "#FFFFFF" if dark else "#1A1A1A"
        accent = TOAST_TYPES[self._toast_type]["color"]
        self._label.setStyleSheet(
            f"color: {text_color}; background: transparent; border: none; font-size: 13px;"
        )
        self._icon_widget.setIcon(TOAST_TYPES[self._toast_type]["icon"])
        self._icon_widget.setStyleSheet(
            f"color: {accent}; background: transparent;"
        )
        self.update()

    @staticmethod
    def show(message, toast_type="info", parent=None):
        toast = Toast(message, toast_type, parent)
        if parent is not None:
            parent_width = parent.width()
            toast_width = min(420, parent_width - 32)
            toast.setFixedWidth(toast_width)
            x = (parent_width - toast_width) // 2
            y = 12
            toast.move(x, y)
        toast.show_toast()
        return toast
