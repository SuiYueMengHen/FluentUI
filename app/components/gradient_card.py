from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPen, QBrush, QPalette


class GradientCard(QFrame):
    @staticmethod
    def _make_transparent(widget):
        widget.setAutoFillBackground(False)
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 0))
        widget.setPalette(palette)
        widget.setStyleSheet(widget.styleSheet() + " background: transparent; background-color: rgba(0,0,0,0);")

    def __init__(self, title="", description="", parent=None,
                 color1="#0078D4", color2="#0067C0", direction="horizontal",
                 auto_layout=True):
        super().__init__(parent)
        self.setAutoFillBackground(False)
        self._title = title
        self._description = description
        self._color1 = color1
        self._color2 = color2
        self._direction = direction
        self._hover_offset = 0.0
        self._border_radius = 12

        self.setFixedHeight(160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(24, 20, 24, 20)

        if auto_layout:
            self._title_label = QLabel(title, self)
            self._title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
            self._title_label.setObjectName("gradientCardTitle")
            self._make_transparent(self._title_label)

            self._desc_label = QLabel(description, self)
            self._desc_label.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 13px;")
            self._desc_label.setWordWrap(True)
            self._desc_label.setObjectName("gradientCardDesc")
            self._make_transparent(self._desc_label)

            self._layout.addWidget(self._title_label)
            self._layout.addStretch()
            self._layout.addWidget(self._desc_label)

        self._anim = QPropertyAnimation(self, b"hoverOffset")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    @property
    def content_layout(self):
        return self._layout

    def get_hover_offset(self):
        return self._hover_offset

    def set_hover_offset(self, val):
        self._hover_offset = val
        self.update()

    hoverOffset = Property(float, get_hover_offset, set_hover_offset)

    def enterEvent(self, event):
        self._anim.setStartValue(self._hover_offset)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.setStartValue(self._hover_offset)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        offset = self._hover_offset * 0.15
        gradient = QLinearGradient()
        if self._direction == "horizontal":
            gradient.setStart(0, 0)
            gradient.setFinalStop(self.width(), self.height())
        else:
            gradient.setStart(0, 0)
            gradient.setFinalStop(0, self.height())

        gradient.setColorAt(0 + offset * 0.3, QColor(self._color1))
        gradient.setColorAt(1 - offset * 0.2, QColor(self._color2))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), self._border_radius, self._border_radius)

        shadow_alpha = int(30 + self._hover_offset * 30)
        painter.setBrush(QColor(0, 0, 0, shadow_alpha))
        painter.drawRoundedRect(self.rect().adjusted(0, 2, 0, 4), self._border_radius, self._border_radius)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
        if hasattr(self, '_title_label'):
            self._make_transparent(self._title_label)
        if hasattr(self, '_desc_label'):
            self._make_transparent(self._desc_label)
