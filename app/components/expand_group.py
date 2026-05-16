from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPalette
from qfluentwidgets import FluentIcon as FIF, IconWidget, isDarkTheme


class _ArrowIcon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rotation = 0.0
        self.setFixedSize(20, 20)

    def get_rotation(self):
        return self._rotation

    def set_rotation(self, val):
        self._rotation = val
        self.update()

    rotation = Property(float, get_rotation, set_rotation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._rotation)
        pixmap = FIF.CHEVRON_RIGHT.icon().pixmap(16, 16)
        painter.drawPixmap(QRectF(-8, -8, 16, 16), pixmap, QRectF(pixmap.rect()))
        painter.end()


class _TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            group = self.parent()
            if isinstance(group, ExpandGroup):
                group.toggle()
        super().mousePressEvent(event)


class ExpandGroup(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self._title = title
        self._expanded = True
        self._expand_progress = 1.0
        self._arrow_rotation = 90.0
        self._border_radius = 12
        self._title_bar_height = 44
        self._content_widget = None
        self._content_height = 0

        self.setAutoFillBackground(False)

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self._title_bar = _TitleBar(self)
        self._title_bar.setMinimumHeight(self._title_bar_height)
        self._title_bar.setMaximumHeight(self._title_bar_height)
        self._title_bar.setCursor(Qt.CursorShape.PointingHandCursor)
        title_layout = QHBoxLayout(self._title_bar)
        title_layout.setContentsMargins(16, 0, 16, 0)

        self._arrow = _ArrowIcon(self._title_bar)
        self._arrow.set_rotation(90.0)
        self._title_label = QLabel(title, self._title_bar)
        self._title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._arrow.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        title_layout.addWidget(self._arrow)
        title_layout.addWidget(self._title_label)
        title_layout.addStretch()

        self._main_layout.addWidget(self._title_bar)

        self._content_area = QWidget(self)
        self._content_layout = QVBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(16, 0, 16, 16)
        self._content_layout.setSpacing(0)
        self._main_layout.addWidget(self._content_area)

        self._expand_anim = QPropertyAnimation(self, b"expandProgress")
        self._expand_anim.setDuration(250)
        self._expand_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._arrow_anim = QPropertyAnimation(self, b"arrowRotation")
        self._arrow_anim.setDuration(250)
        self._arrow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.refresh_theme()

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress(self, val):
        self._expand_progress = val
        target = self._content_height if self._content_height > 0 else 100
        if val >= 1.0:
            self._content_area.setMaximumHeight(16777215)
        elif val <= 0.0:
            self._content_area.setMaximumHeight(0)
        else:
            self._content_area.setMaximumHeight(int(target * val))
        self.update()

    expandProgress = Property(float, get_expand_progress, set_expand_progress)

    def get_arrow_rotation(self):
        return self._arrow_rotation

    def set_arrow_rotation(self, val):
        self._arrow_rotation = val
        self._arrow.set_rotation(val)
        self.update()

    arrowRotation = Property(float, get_arrow_rotation, set_arrow_rotation)

    def set_content(self, widget):
        if self._content_layout.count() > 0:
            old = self._content_layout.takeAt(0).widget()
            if old:
                old.deleteLater()
        self._content_layout.addWidget(widget)
        self._content_widget = widget
        widget.adjustSize()
        content_h = widget.sizeHint().height()
        margins = self._content_layout.contentsMargins()
        self._content_height = content_h + margins.top() + margins.bottom()
        if self._expanded:
            self._content_area.setMaximumHeight(16777215)
        else:
            self._content_area.setMaximumHeight(0)

    def set_expanded(self, expanded, animate=True):
        if self._expanded == expanded:
            return
        self._expanded = expanded
        if animate:
            self._expand_anim.setStartValue(self._expand_progress)
            self._expand_anim.setEndValue(1.0 if expanded else 0.0)
            self._expand_anim.start()

            self._arrow_anim.setStartValue(self._arrow_rotation)
            self._arrow_anim.setEndValue(90.0 if expanded else 0.0)
            self._arrow_anim.start()
        else:
            self._expand_progress = 1.0 if expanded else 0.0
            self._arrow_rotation = 90.0 if expanded else 0.0
            self._arrow.set_rotation(self._arrow_rotation)
            if expanded:
                self._content_area.setMaximumHeight(16777215)
            else:
                self._content_area.setMaximumHeight(0)
            self.update()

    def toggle(self):
        self.set_expanded(not self._expanded)

    def is_expanded(self):
        return self._expanded

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border = QColor(255, 255, 255, int(255 * 0.08)) if dark else QColor(0, 0, 0, int(255 * 0.1))

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, self._border_radius, self._border_radius)

        painter.end()

    def refresh_theme(self):
        dark = isDarkTheme()
        text_color = "#FFFFFF" if dark else "#1A1A1A"
        self._title_label.setStyleSheet(
            f"color: {text_color}; font-size: 14px; font-weight: 600; background: transparent;"
        )
        self._title_bar.setStyleSheet("background: transparent;")
        self._content_area.setStyleSheet("background: transparent;")
        self._arrow.update()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() < self._title_bar_height:
                self.toggle()
        super().mousePressEvent(event)
