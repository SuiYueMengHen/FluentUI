from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient
from qfluentwidgets import FluentIcon, IconWidget, isDarkTheme


class StatCard(QFrame):
    def __init__(self, title="", value="", icon=FluentIcon.APPLICATION, trend="",
                 accent_color="#0078D4", parent=None):
        super().__init__(parent)
        self._title = title
        self._value = value
        self._icon = icon
        self._trend = trend
        self._accent_color = accent_color
        self._hover_offset = 0.0

        self.setFixedHeight(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("statCard")

        self._anim = QPropertyAnimation(self, b"hoverOffset")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)

        top_row = QHBoxLayout()
        self._icon_label = IconWidget(icon, self)
        self._icon_label.setFixedSize(24, 24)
        top_row.addWidget(self._icon_label)
        top_row.addStretch()

        if trend:
            trend_color = "#6CCB5F" if "↑" in trend or "+" in trend else "#FF6B6B"
            self._trend_label = QLabel(trend, self)
            self._trend_label.setStyleSheet(
                f"color: {trend_color}; font-size: 12px; font-weight: 600; background: transparent;"
            )
            top_row.addWidget(self._trend_label)

        layout.addLayout(top_row)

        self._value_label = QLabel(value, self)
        self._update_value_style()
        layout.addWidget(self._value_label)

        self._title_label = QLabel(title, self)
        self._update_title_style()
        layout.addWidget(self._title_label)

    def _update_value_style(self):
        color = "#1A1A1A" if not self.is_dark() else "#FFFFFF"
        self._value_label.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {color}; background: transparent;")

    def _update_title_style(self):
        color = "#9E9E9E" if self.is_dark() else "#616161"
        self._title_label.setStyleSheet(f"font-size: 12px; color: {color}; background: transparent;")

    def refresh_theme(self):
        self._update_value_style()
        self._update_title_style()
        self.update()

    def get_hover_offset(self):
        return self._hover_offset

    def set_hover_offset(self, val):
        self._hover_offset = val
        self.update()

    hoverOffset = Property(float, get_hover_offset, set_hover_offset)

    def enterEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._hover_offset)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._hover_offset)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor("#FFFFFF") if not self.is_dark() else QColor("#2D2D2D")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        r = self.rect()
        painter.drawRoundedRect(r, 12, 12)

        accent = QColor(self._accent_color)
        accent.setAlpha(int(20 + self._hover_offset * 30))
        painter.setBrush(accent)
        painter.drawRoundedRect(r, 12, 12)

        bar_rect = r.adjusted(0, 0, -r.width() + 4, 0)
        gradient = QLinearGradient(0, 0, 0, r.height())
        gradient.setColorAt(0, QColor(self._accent_color))
        gradient.setColorAt(1, QColor(self._accent_color).darker(120))
        painter.setBrush(gradient)
        painter.drawRoundedRect(bar_rect, 2, 2)

        painter.end()

    def is_dark(self):
        return isDarkTheme()
