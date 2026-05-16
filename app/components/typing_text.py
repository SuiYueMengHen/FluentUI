from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPen


class TypingText(QLabel):
    def __init__(self, full_text="", typing_speed=60, parent=None, loop=False):
        super().__init__(parent)
        self._full_text = full_text
        self._typing_speed = typing_speed
        self._loop = loop
        self._current_index = 0
        self._cursor_visible = True
        self._is_typing = False

        self._typing_timer = QTimer(self)
        self._typing_timer.timeout.connect(self._type_next_char)

        self._cursor_timer = QTimer(self)
        self._cursor_timer.timeout.connect(self._toggle_cursor)

        self.setText("")

    def showEvent(self, event):
        super().showEvent(event)
        self._cursor_timer.start(530)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._cursor_timer.stop()
        self._typing_timer.stop()

    def set_text(self, text: str):
        self._full_text = text
        self._current_index = 0
        self.setText("")
        self.start_typing()

    def start_typing(self):
        self._is_typing = True
        self._current_index = 0
        self.setText("")
        self._typing_timer.start(self._typing_speed)

    def stop_typing(self):
        self._is_typing = False
        self._typing_timer.stop()
        self.setText(self._full_text)

    def _type_next_char(self):
        if self._current_index < len(self._full_text):
            self._current_index += 1
            displayed = self._full_text[:self._current_index]
            if self._cursor_visible:
                displayed += "|"
            self.setText(displayed)
        else:
            if self._loop:
                self._current_index = 0
                self.setText("")
            else:
                self._is_typing = False
                self._typing_timer.stop()
                self.setText(self._full_text)

    def _toggle_cursor(self):
        self._cursor_visible = not self._cursor_visible
        if self._is_typing:
            displayed = self._full_text[:self._current_index]
            if self._cursor_visible:
                displayed += "|"
            self.setText(displayed)
