from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class ChartTooltip(QFrame):
    def __init__(self, title="", values=None, parent=None):
        super().__init__(parent)
        self._title = title
        self._values = values or []
        self._opacity = 0.0
        self._anim = QPropertyAnimation(self, b"tooltipOpacity")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)

    def _is_dark(self):
        return isDarkTheme()

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, val):
        self._opacity = val
        self.update()

    tooltipOpacity = Property(float, get_opacity, set_opacity)

    def set_title(self, title):
        self._title = title
        self.update()

    def set_values(self, values):
        self._values = list(values)
        self._adjust_size()
        self.update()

    def _adjust_size(self):
        row_h = 24
        title_h = 28 if self._title else 0
        padding = 16
        w = 200
        h = padding * 2 + title_h + len(self._values) * row_h
        self.setFixedSize(w, max(h, 60))

    def show_at(self, pos):
        self._adjust_size()
        self.move(pos.toPoint())
        self.show()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def hide_tooltip(self):
        self._anim.setStartValue(self._opacity)
        self._anim.setEndValue(0.0)
        self._anim.start()
        QTimer.singleShot(200, self.hide)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity)

        is_dark = self._is_dark()
        bg = QColor("#FFFFFF") if not is_dark else QColor("#2D2D2D")
        border = QColor("#E0E0E0") if not is_dark else QColor("#3D3D3D")
        text_color = QColor("#1A1A1A") if not is_dark else QColor("#FFFFFF")
        dim_color = QColor("#616161") if not is_dark else QColor("#9E9E9E")

        r = QRectF(0, 0, self.width(), self.height())

        shadow_path = QPainterPath()
        shadow_path.addRoundedRect(r.adjusted(2, 2, 2, 2), 8, 8)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 40))
        painter.drawPath(shadow_path)

        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(r, 8, 8)

        y_offset = 16.0

        if self._title:
            font = painter.font()
            font.setPointSize(11)
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(text_color)
            title_rect = QRectF(16, y_offset, self.width() - 32, 20)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._title)
            y_offset += 28

        font = painter.font()
        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)

        for val in self._values:
            color = QColor(val.get("color", "#0078D4"))
            dot_rect = QRectF(16, y_offset + 6, 8, 8)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(dot_rect)

            name = val.get("name", "")
            name_rect = QRectF(30, y_offset, 90, 20)
            painter.setPen(dim_color)
            painter.drawText(name_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, name)

            value = val.get("value", "")
            value_rect = QRectF(120, y_offset, self.width() - 136, 20)
            painter.setPen(text_color)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(value_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, value)
            font.setBold(False)
            painter.setFont(font)

            y_offset += 24

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
