from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import isDarkTheme


class OTPInput(QWidget):
    otpComplete = Signal(str)

    def __init__(self, length=6, parent=None):
        super().__init__(parent)
        self._length = length
        self._digits = [""] * length
        self._focus_index = 0
        self._box_scale = [1.0] * length
        self._anim_index = -1
        self._anim_value = 1.0
        self._active_anims = []
        self.setFixedSize(length * 52 + (length - 1) * 8, 64)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def _is_dark(self):
        return isDarkTheme()

    def get_anim_value(self):
        return self._anim_value

    def set_anim_value(self, val):
        self._anim_value = val
        if 0 <= self._anim_index < len(self._box_scale):
            self._box_scale[self._anim_index] = val
            self.update()

    animValue = Property(float, get_anim_value, set_anim_value)

    def _box_rect(self, index):
        x = index * 52 + index * 8
        return QRectF(x, 8, 44, 48)

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            digit = str(key - Qt.Key.Key_0)
            if self._focus_index < self._length:
                self._digits[self._focus_index] = digit
                self._animate_box(self._focus_index)
                if self._focus_index < self._length - 1:
                    self._focus_index += 1
                self.update()
                if all(d for d in self._digits):
                    self.otpComplete.emit("".join(self._digits))
        elif key == Qt.Key.Key_Backspace:
            if self._focus_index > 0 and self._digits[self._focus_index] == "":
                self._focus_index -= 1
            self._digits[self._focus_index] = ""
            self.update()
        elif key == Qt.Key.Key_Left:
            self._focus_index = max(0, self._focus_index - 1)
            self.update()
        elif key == Qt.Key.Key_Right:
            self._focus_index = min(self._length - 1, self._focus_index + 1)
            self.update()

    def _animate_box(self, index):
        self._anim_index = index
        anim = QPropertyAnimation(self, b"animValue")
        anim.setParent(self)
        anim.setDuration(150)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.setStartValue(1.05)
        anim.setEndValue(1.0)
        anim.finished.connect(lambda: self._cleanup_anim(anim))
        anim.start()
        self._active_anims.append(anim)

    def _cleanup_anim(self, anim):
        if anim in self._active_anims:
            self._active_anims.remove(anim)

    def mousePressEvent(self, event):
        pos = event.position()
        for i in range(self._length):
            if self._box_rect(i).contains(pos):
                self._focus_index = i
                self.update()
                break

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        focus_border = QColor("#0078D4")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        digit_bg = QColor("#1E1E1E") if is_dark else QColor("#F5F5F5")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        for i in range(self._length):
            rect = self._box_rect(i)
            scale = self._box_scale[i]
            cx = rect.center().x()
            cy = rect.center().y()

            painter.save()
            painter.translate(cx, cy)
            painter.scale(scale, scale)
            painter.translate(-cx, -cy)

            painter.setBrush(digit_bg)
            is_focused = (i == self._focus_index)
            pen = QPen(focus_border, 2) if is_focused else QPen(border_color, 1)
            painter.setPen(pen)
            painter.drawRoundedRect(rect, 6, 6)

            if self._digits[i]:
                painter.setPen(text_color)
                font = painter.font()
                font.setPointSize(18)
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self._digits[i])
            elif is_focused:
                cursor_x = rect.center().x()
                cursor_y1 = rect.y() + 14
                cursor_y2 = rect.bottom() - 14
                painter.setPen(QPen(focus_border, 2))
                painter.drawLine(int(cursor_x), int(cursor_y1), int(cursor_x), int(cursor_y2))

            painter.restore()

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
