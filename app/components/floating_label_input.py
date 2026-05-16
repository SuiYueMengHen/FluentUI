from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class FloatingLabelInput(QWidget):
    def __init__(self, label="", placeholder="", parent=None):
        super().__init__(parent)
        self._label = label
        self._placeholder = placeholder
        self._label_offset = 1.0
        self._focused = False
        self._has_text = False
        self.setFixedSize(280, 56)

        self._line_edit = QLineEdit(self)
        self._line_edit.setGeometry(12, 18, 256, 30)
        self._line_edit.setStyleSheet("background: transparent; border: none; outline: none;")
        self._line_edit.textChanged.connect(self._on_text_changed)
        self._line_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._label_anim = QPropertyAnimation(self, b"labelOffset")
        self._label_anim.setDuration(200)
        self._label_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_label_offset(self):
        return self._label_offset

    def set_label_offset(self, val):
        self._label_offset = val
        self.update()

    labelOffset = Property(float, get_label_offset, set_label_offset)

    def _is_dark(self):
        return isDarkTheme()

    def _on_text_changed(self, text):
        self._has_text = len(text) > 0
        if self._has_text and not self._focused:
            self._float_up()
        elif not self._has_text and not self._focused:
            self._float_down()

    def _float_up(self):
        self._label_anim.setStartValue(self._label_offset)
        self._label_anim.setEndValue(0.0)
        self._label_anim.start()

    def _float_down(self):
        self._label_anim.setStartValue(self._label_offset)
        self._label_anim.setEndValue(1.0)
        self._label_anim.start()

    def focusInEvent(self, event):
        self._focused = True
        self._float_up()
        self._line_edit.setFocus()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._focused = False
        if not self._has_text:
            self._float_down()
        super().focusOutEvent(event)

    def text(self):
        return self._line_edit.text()

    def setText(self, text):
        self._line_edit.setText(text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor("#0078D4") if self._focused else (QColor("#555555") if is_dark else QColor("#CCCCCC"))
        label_color = QColor("#0078D4") if (self._focused or self._has_text) else (QColor("#AAAAAA") if is_dark else QColor("#888888"))
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        placeholder_color = QColor("#666666") if is_dark else QColor("#AAAAAA")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        border_y = 48
        painter.setPen(QPen(border_color, 2 if self._focused else 1))
        painter.drawLine(12, border_y, 268, border_y)

        label_y = 14 + self._label_offset * 18
        font = painter.font()
        font.setPointSize(10 if (self._focused or self._has_text) else 12)
        painter.setFont(font)
        painter.setPen(label_color)
        painter.drawText(QRectF(12, label_y, 256, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._label)

        if not self._has_text and not self._focused:
            painter.setPen(placeholder_color)
            font.setPointSize(12)
            painter.setFont(font)
            painter.drawText(QRectF(12, 22, 256, 24), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._placeholder)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
