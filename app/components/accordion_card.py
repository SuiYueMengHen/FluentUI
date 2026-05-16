from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPalette
from qfluentwidgets import FluentIcon as FIF, IconWidget, isDarkTheme


class _ArrowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rotation = 0.0
        self.setFixedSize(20, 20)

    def set_rotation(self, rotation):
        self._rotation = rotation
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._rotation)
        icon = FIF.DOWN.icon()
        pixmap = icon.pixmap(16, 16)
        painter.drawPixmap(-8, -8, pixmap)
        painter.end()


class AccordionCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        self._subtitle = ""
        self._expand_progress = 0.0
        self._arrow_rotation = 0.0
        self._is_expanded = False
        self._is_hovered = False
        self._content_widget = None
        self._content_height = 0
        self._title_bar_height = 48

        self._animation = QPropertyAnimation(self, b"expand_progress")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.finished.connect(self._on_animation_finished)

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumWidth(200)

        self._setup_ui()
        self.refresh_theme()

    def _setup_ui(self):
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self._title_bar = QWidget(self)
        self._title_bar.setMinimumHeight(44)
        self._title_bar.setFixedHeight(self._title_bar_height)
        self._title_bar.setCursor(Qt.CursorShape.PointingHandCursor)

        title_layout = QHBoxLayout(self._title_bar)
        title_layout.setContentsMargins(16, 0, 16, 0)
        title_layout.setSpacing(8)

        self._arrow_widget = _ArrowWidget(self._title_bar)
        title_layout.addWidget(self._arrow_widget)

        self._title_label = QLabel(self._title, self._title_bar)
        title_layout.addWidget(self._title_label)

        self._subtitle_label = QLabel("", self._title_bar)
        self._subtitle_label.setVisible(False)
        title_layout.addWidget(self._subtitle_label)
        title_layout.addStretch()

        self._main_layout.addWidget(self._title_bar)

        self._content_container = QWidget(self)
        self._content_layout = QVBoxLayout(self._content_container)
        self._content_layout.setContentsMargins(20, 0, 16, 12)
        self._content_layout.setSpacing(0)
        self._content_container.setMaximumHeight(0)
        self._content_container.setVisible(False)

        self._main_layout.addWidget(self._content_container)

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress_internal(self, progress):
        self._expand_progress = progress
        self._arrow_rotation = progress * 180.0
        self._arrow_widget.set_rotation(self._arrow_rotation)

        content_h = int(self._content_height * progress)
        self._content_container.setMaximumHeight(content_h)

        if progress > 0:
            self._content_container.setVisible(True)

        self.update()

    expand_progress = Property(float, get_expand_progress, set_expand_progress_internal)

    def _on_animation_finished(self):
        if not self._is_expanded:
            self._content_container.setVisible(False)

    def set_content(self, widget: QWidget):
        if self._content_widget:
            self._content_layout.removeWidget(self._content_widget)
            self._content_widget.deleteLater()

        self._content_widget = widget
        self._content_layout.addWidget(widget)
        self._content_height = max(widget.sizeHint().height(), 100)

        if self._is_expanded:
            self._content_container.setMaximumHeight(self._content_height)
            self._content_container.setVisible(True)
        else:
            self._content_container.setMaximumHeight(0)
            self._content_container.setVisible(False)

    def set_expanded(self, expanded: bool, animate=True):
        if self._is_expanded == expanded:
            return

        self._is_expanded = expanded

        if self._content_widget:
            self._content_height = max(self._content_widget.sizeHint().height(), 100)

        if animate:
            self._animation.stop()
            if expanded:
                self._animation.setStartValue(self._expand_progress)
                self._animation.setEndValue(1.0)
                self._content_container.setVisible(True)
            else:
                self._animation.setStartValue(self._expand_progress)
                self._animation.setEndValue(0.0)
            self._animation.start()
        else:
            if expanded:
                self.set_expand_progress_internal(1.0)
                self._content_container.setVisible(True)
            else:
                self.set_expand_progress_internal(0.0)
                self._content_container.setVisible(False)

    def toggle(self):
        self.set_expanded(not self._is_expanded)

    def is_expanded(self) -> bool:
        return self._is_expanded

    def set_subtitle(self, subtitle: str):
        self._subtitle = subtitle
        self._subtitle_label.setText(subtitle)
        self._subtitle_label.setVisible(bool(subtitle))

    def is_dark(self):
        return isDarkTheme()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = self.is_dark()
        bg_color = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border_color = QColor(255, 255, 255, 20) if dark else QColor(0, 0, 0, 25)
        accent_color = QColor("#0078D4")

        rect = QRectF(self.rect())
        radius = 8.0

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(rect, radius, radius)

        painter.save()
        painter.setClipRect(QRectF(0, 0, 4, rect.height()))
        painter.setBrush(accent_color)
        painter.drawRoundedRect(rect, radius, radius)
        painter.restore()

        if self._is_hovered:
            hover_color = QColor(255, 255, 255, 10) if dark else QColor(0, 0, 0, 8)
            painter.save()
            painter.setClipRect(QRectF(0, 0, rect.width(), self._title_bar_height))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(hover_color)
            painter.drawRoundedRect(rect, radius, radius)
            painter.restore()

        painter.setPen(QPen(border_color, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)

        painter.end()

    def refresh_theme(self):
        dark = self.is_dark()
        text_color = "#FFFFFF" if dark else "#1A1A1A"
        secondary_color = "#9E9E9E" if dark else "#616161"

        self._title_label.setStyleSheet(
            f"color: {text_color}; font-size: 14px; font-weight: 600; background: transparent;"
        )
        self._subtitle_label.setStyleSheet(
            f"color: {secondary_color}; font-size: 12px; background: transparent;"
        )
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            title_bar_rect = self._title_bar.geometry()
            if title_bar_rect.contains(event.position().toPoint()):
                self.toggle()
                return
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self._is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)
