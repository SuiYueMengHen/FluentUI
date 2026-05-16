from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPainterPath, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class CreditCardInput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._card_number = ""
        self._card_name = ""
        self._card_expiry = ""
        self._card_cvv = ""
        self._flip_progress = 0.0
        self._show_cvv = False
        self.setFixedSize(360, 240)

        self._number_input = QLineEdit(self)
        self._number_input.setGeometry(20, 180, 200, 28)
        self._number_input.setPlaceholderText("Card Number")
        self._number_input.setMaxLength(19)
        self._number_input.setStyleSheet("background: transparent; border: none; color: transparent;")
        self._number_input.textChanged.connect(self._on_number_changed)

        self._name_input = QLineEdit(self)
        self._name_input.setGeometry(20, 210, 140, 28)
        self._name_input.setPlaceholderText("Name")
        self._name_input.setStyleSheet("background: transparent; border: none; color: transparent;")
        self._name_input.textChanged.connect(self._on_name_changed)

        self._expiry_input = QLineEdit(self)
        self._expiry_input.setGeometry(170, 210, 50, 28)
        self._expiry_input.setPlaceholderText("MM/YY")
        self._expiry_input.setMaxLength(5)
        self._expiry_input.setStyleSheet("background: transparent; border: none; color: transparent;")
        self._expiry_input.textChanged.connect(self._on_expiry_changed)

        self._cvv_input = QLineEdit(self)
        self._cvv_input.setGeometry(240, 210, 60, 28)
        self._cvv_input.setPlaceholderText("CVV")
        self._cvv_input.setMaxLength(3)
        self._cvv_input.setStyleSheet("background: transparent; border: none; color: transparent;")
        self._cvv_input.textChanged.connect(self._on_cvv_changed)

        self._flip_anim = QPropertyAnimation(self, b"flipProgress")
        self._flip_anim.setDuration(300)
        self._flip_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_flip_progress(self):
        return self._flip_progress

    def set_flip_progress(self, val):
        self._flip_progress = val
        self.update()

    flipProgress = Property(float, get_flip_progress, set_flip_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _on_number_changed(self, text):
        self._card_number = text
        self.update()

    def _on_name_changed(self, text):
        self._card_name = text
        self.update()

    def _on_expiry_changed(self, text):
        self._card_expiry = text
        self.update()

    def _on_cvv_changed(self, text):
        self._card_cvv = text
        self.update()

    def _flip_to_cvv(self):
        self._show_cvv = True
        self._flip_anim.setStartValue(0.0)
        self._flip_anim.setEndValue(1.0)
        self._flip_anim.start()

    def _flip_to_front(self):
        self._show_cvv = False
        self._flip_anim.setStartValue(1.0)
        self._flip_anim.setEndValue(0.0)
        self._flip_anim.start()

    def _card_rect(self):
        return QRectF(20, 10, 320, 160)

    def _get_card_type_icon(self):
        num = self._card_number.replace(" ", "")
        if num.startswith("4"):
            return "VISA"
        elif num.startswith(("51", "52", "53", "54", "55")):
            return "MC"
        elif num.startswith(("34", "37")):
            return "AMEX"
        return "CARD"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()

        card_rect = self._card_rect()
        cx = card_rect.center().x()
        cy = card_rect.center().y()

        flip_val = self._flip_progress
        show_back = flip_val > 0.5
        scale_x = abs(1.0 - flip_val * 2) if flip_val <= 0.5 else abs(flip_val * 2 - 1.0)
        scale_x = max(0.01, scale_x)

        painter.save()
        painter.translate(cx, cy)
        painter.scale(scale_x, 1.0)
        painter.translate(-cx, -cy)

        if show_back:
            grad = QLinearGradient(card_rect.topLeft(), card_rect.bottomRight())
            if is_dark:
                grad.setColorAt(0, QColor("#1A3A5C"))
                grad.setColorAt(1, QColor("#0D2137"))
            else:
                grad.setColorAt(0, QColor("#2B5EA7"))
                grad.setColorAt(1, QColor("#1A3D6F"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(grad)
            painter.drawRoundedRect(card_rect, 12, 12)

            stripe_rect = QRectF(card_rect.x(), card_rect.y() + 30, card_rect.width(), 36)
            painter.setBrush(QColor("#1A1A1A"))
            painter.drawRect(stripe_rect)

            cvv_rect = QRectF(card_rect.right() - 100, card_rect.y() + 80, 80, 28)
            painter.setBrush(QColor("#FFFFFF"))
            painter.drawRoundedRect(cvv_rect, 4, 4)
            painter.setPen(QColor("#1A1A1A"))
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(cvv_rect, Qt.AlignmentFlag.AlignCenter, self._card_cvv or "CVV")
        else:
            grad = QLinearGradient(card_rect.topLeft(), card_rect.bottomRight())
            if is_dark:
                grad.setColorAt(0, QColor("#1A3A5C"))
                grad.setColorAt(1, QColor("#0D2137"))
            else:
                grad.setColorAt(0, QColor("#2B5EA7"))
                grad.setColorAt(1, QColor("#1A3D6F"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(grad)
            painter.drawRoundedRect(card_rect, 12, 12)

            chip_rect = QRectF(card_rect.x() + 24, card_rect.y() + 40, 40, 28)
            painter.setBrush(QColor("#D4AF37"))
            painter.drawRoundedRect(chip_rect, 4, 4)

            painter.setPen(QColor("#FFFFFF"))
            font = painter.font()
            font.setPointSize(14)
            font.setBold(True)
            painter.setFont(font)
            display_num = self._card_number or "•••• •••• •••• ••••"
            painter.drawText(QRectF(card_rect.x() + 24, card_rect.y() + 80, 270, 24),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, display_num)

            font.setPointSize(9)
            font.setBold(False)
            painter.setFont(font)
            painter.drawText(QRectF(card_rect.x() + 24, card_rect.y() + 115, 160, 16),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                           self._card_name.upper() or "CARDHOLDER NAME")

            painter.drawText(QRectF(card_rect.right() - 80, card_rect.y() + 115, 56, 16),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                           self._card_expiry or "MM/YY")

            card_type = self._get_card_type_icon()
            font.setPointSize(10)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(QRectF(card_rect.right() - 70, card_rect.y() + 14, 50, 20),
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, card_type)

        painter.restore()
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
