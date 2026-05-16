from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ColorTagInput(QWidget):
    tagsChanged = Signal(list)

    def __init__(self, tags=None, parent=None):
        super().__init__(parent)
        self._tags = tags or []
        self._pop_progress = 1.0
        self._hovered_close = -1
        self.setMinimumSize(300, 40)
        self.setFixedHeight(40)

        self._input = QLineEdit(self)
        self._input.setStyleSheet("background: transparent; border: none;")
        self._input.setPlaceholderText("Add tag...")
        self._input.returnPressed.connect(self._add_tag)
        self._input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

        self._pop_anim = QPropertyAnimation(self, b"popProgress")
        self._pop_anim.setDuration(150)
        self._pop_anim.setStartValue(0.0)
        self._pop_anim.setEndValue(1.0)
        self._pop_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_pop_progress(self):
        return self._pop_progress

    def set_pop_progress(self, val):
        self._pop_progress = val
        self.update()

    popProgress = Property(float, get_pop_progress, set_pop_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _add_tag(self):
        text = self._input.text().strip()
        if text:
            colors = ["#0078D4", "#107C10", "#B4009E", "#D83B01", "#008272", "#5C2D91"]
            color = colors[len(self._tags) % len(colors)]
            self._tags.append({"text": text, "color": color})
            self._input.clear()
            self._pop_anim.setStartValue(0.0)
            self._pop_anim.setEndValue(1.0)
            self._pop_anim.start()
            self.tagsChanged.emit(self._tags)
            self.update()

    def _remove_tag(self, index):
        if 0 <= index < len(self._tags):
            self._tags.pop(index)
            self.tagsChanged.emit(self._tags)
            self.update()

    def _tag_rects(self):
        rects = []
        x = 8
        for tag in self._tags:
            text = tag.get("text", "")
            w = max(60, len(text) * 8 + 36)
            rects.append(QRectF(x, 6, w, 28))
            x += w + 6
        return rects

    def resizeEvent(self, event):
        tag_rects = self._tag_rects()
        if tag_rects:
            last = tag_rects[-1]
            input_x = int(last.right() + 8)
        else:
            input_x = 8
        self._input.setGeometry(input_x, 6, max(80, self.width() - input_x - 8), 28)
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        pos = event.position()
        for i, rect in enumerate(self._tag_rects()):
            close_rect = QRectF(rect.right() - 20, rect.y(), 20, rect.height())
            if close_rect.contains(pos):
                self._remove_tag(i)
                return

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_close = -1
        for i, rect in enumerate(self._tag_rects()):
            close_rect = QRectF(rect.right() - 20, rect.y(), 20, rect.height())
            if close_rect.contains(pos):
                self._hovered_close = i
                break
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        tag_bg_alpha = 0.2

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        tag_rects = self._tag_rects()
        for i, (rect, tag) in enumerate(zip(tag_rects, self._tags)):
            color = QColor(tag.get("color", "#0078D4"))
            tag_bg = QColor(color)
            tag_bg.setAlphaF(tag_bg_alpha if is_dark else 0.12)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(tag_bg)
            painter.drawRoundedRect(rect, 14, 14)

            dot_rect = QRectF(rect.x() + 8, rect.center().y() - 4, 8, 8)
            painter.setBrush(color)
            painter.drawEllipse(dot_rect)

            painter.setPen(text_color)
            font = painter.font()
            font.setPointSize(9)
            painter.setFont(font)
            text_w = rect.width() - 36
            painter.drawText(QRectF(rect.x() + 20, rect.y(), text_w, rect.height()),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, tag.get("text", ""))

            close_rect = QRectF(rect.right() - 20, rect.y(), 20, rect.height())
            close_color = QColor("#FF4444") if self._hovered_close == i else (QColor("#AAAAAA") if is_dark else QColor("#888888"))
            painter.setPen(close_color)
            font.setPointSize(10)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(close_rect, Qt.AlignmentFlag.AlignCenter, "×")

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
