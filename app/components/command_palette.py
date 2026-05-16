from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class CommandPalette(QWidget):
    commandSelected = Signal(str)

    def __init__(self, commands=None, parent=None):
        super().__init__(parent)
        self._commands = []
        if commands:
            for c in commands:
                if isinstance(c, str):
                    self._commands.append({"name": c, "action": c.lower().replace(" ", "_"), "icon": FIF.SEARCH})
                else:
                    self._commands.append(c)
        self._opacity = 0.0
        self._filtered = list(self._commands)
        self._hovered_index = -1
        self._search_text = ""
        self.setFixedSize(420, 360)
        self._anim = QPropertyAnimation(self, b"opacity")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._search_input = QLineEdit(self)
        self._search_input.setPlaceholderText("Type a command...")
        self._search_input.setGeometry(16, 12, 388, 36)
        self._search_input.textChanged.connect(self._on_search)
        self._search_input.setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 8px; padding: 6px 12px; font-size: 13px; }")
        self.setMouseTracking(True)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, val):
        self._opacity = val
        self.update()

    opacity = Property(float, get_opacity, set_opacity)

    def _on_search(self, text):
        self._search_text = text
        self._filtered = [c for c in self._commands if text.lower() in c.get("name", "").lower()]
        self._hovered_index = -1
        self.update()

    def show_palette(self):
        self._opacity = 0.0
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()
        self.show()
        self._search_input.setFocus()

    def hide_palette(self):
        self._opacity = 1.0
        self._anim.stop()
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(0.0)
        self._anim.start()
        QTimer.singleShot(200, self.hide)

    def mouseMoveEvent(self, event):
        y = event.position().y()
        item_y_start = 56
        item_h = 36
        idx = int((y - item_y_start) / item_h)
        if 0 <= idx < len(self._filtered):
            self._hovered_index = idx
        else:
            self._hovered_index = -1
        self.update()

    def mousePressEvent(self, event):
        if self._hovered_index >= 0 and self._hovered_index < len(self._filtered):
            cmd = self._filtered[self._hovered_index]
            self.commandSelected.emit(cmd.get("action", ""))
            self.hide_palette()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity)
        dark = isDarkTheme()
        bg = QColor("#2D2D2D") if dark else QColor("#FFFFFF")
        border = QColor("#505050") if dark else QColor("#D0D0D0")
        text_color = QColor("#FFFFFF") if dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if dark else QColor("#888888")
        hover_bg = QColor("#3D3D3D") if dark else QColor("#F0F0F0")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        pen = QPen(border, 1)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        item_y = 56
        item_h = 36
        for i, cmd in enumerate(self._filtered):
            if item_y + item_h > self.height():
                break
            if i == self._hovered_index:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(hover_bg)
                painter.drawRoundedRect(QRectF(8, item_y, self.width() - 16, item_h), 6, 6)
            icon = cmd.get("icon", FIF.SEARCH)
            icon.icon().paint(painter, QRectF(20, item_y + 8, 20, 20).toRect())
            painter.setPen(text_color)
            font = QFont()
            font.setPointSize(11)
            painter.setFont(font)
            painter.drawText(QRectF(48, item_y, self.width() - 120, item_h), Qt.AlignmentFlag.AlignVCenter, cmd.get("name", ""))
            shortcut = cmd.get("shortcut", "")
            if shortcut:
                painter.setPen(sub_color)
                font.setPointSize(9)
                painter.setFont(font)
                painter.drawText(QRectF(self.width() - 90, item_y, 80, item_h), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, shortcut)
            item_y += item_h
        painter.end()

    def refresh_theme(self):
        dark = isDarkTheme()
        if dark:
            self._search_input.setStyleSheet("QLineEdit { border: 1px solid #505050; border-radius: 8px; padding: 6px 12px; font-size: 13px; background: #2D2D2D; color: #FFFFFF; }")
        else:
            self._search_input.setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 8px; padding: 6px 12px; font-size: 13px; }")
        self.update()
        self.repaint()
