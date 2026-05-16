from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPalette
from qfluentwidgets import isDarkTheme


class SegmentedWidget(QWidget):
    currentChanged = Signal(int)

    def __init__(self, segments=None, parent=None):
        super().__init__(parent)
        self._segments = segments or []
        self._current_index = 0
        self._indicator_x = 0.0
        self._indicator_width = 0.0

        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(0)

        self._anim = QPropertyAnimation(self, b"indicatorPos")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._width_anim = QPropertyAnimation(self, b"indicatorSize")
        self._width_anim.setDuration(200)
        self._width_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        if self._segments:
            self._update_indicator_target(0, animate=False)

    def _is_dark(self):
        return isDarkTheme()

    def _get_colors(self):
        if self._is_dark():
            return {
                "bg": QColor("#2D2D2D"),
                "indicator": QColor("#3D3D3D"),
                "text": QColor("#FFFFFF"),
                "secondary_text": QColor("#9E9E9E"),
                "border": QColor(255, 255, 255, 20),
            }
        return {
            "bg": QColor("#F0F0F0"),
            "indicator": QColor("#FFFFFF"),
            "text": QColor("#1A1A1A"),
            "secondary_text": QColor("#616161"),
            "border": QColor(0, 0, 0, 25),
        }

    def get_indicator_x(self):
        return self._indicator_x

    def set_indicator_x(self, val):
        self._indicator_x = val
        self.update()

    indicatorPos = Property(float, get_indicator_x, set_indicator_x)

    def get_indicator_width(self):
        return self._indicator_width

    def set_indicator_width(self, val):
        self._indicator_width = val
        self.update()

    indicatorSize = Property(float, get_indicator_width, set_indicator_width)

    def set_segments(self, segments):
        self._segments = list(segments)
        self._current_index = 0
        self._update_indicator_target(0, animate=False)
        self.update()

    def set_current_index(self, index):
        if 0 <= index < len(self._segments) and index != self._current_index:
            self._current_index = index
            self._update_indicator_target(index, animate=True)
            self.currentChanged.emit(index)

    def get_current_index(self):
        return self._current_index

    def _segment_width(self):
        if not self._segments:
            return 0
        return self.width() / len(self._segments)

    def _update_indicator_target(self, index, animate=True):
        seg_w = self._segment_width()
        target_x = index * seg_w

        if animate:
            self._anim.setStartValue(self._indicator_x)
            self._anim.setEndValue(target_x)
            self._anim.start()

            self._width_anim.setStartValue(self._indicator_width)
            self._width_anim.setEndValue(seg_w)
            self._width_anim.start()
        else:
            self._indicator_x = target_x
            self._indicator_width = seg_w
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        colors = self._get_colors()
        w = self.width()
        h = self.height()

        bg_rect = QRectF(0, 0, w, h)
        painter.setPen(QPen(colors["border"], 1))
        painter.setBrush(colors["bg"])
        painter.drawRoundedRect(bg_rect, 10, 10)

        if self._segments:
            seg_w = self._segment_width()
            indicator_rect = QRectF(
                self._indicator_x + 2,
                2,
                self._indicator_width - 4,
                h - 4,
            )
            painter.setPen(Qt.PenStyle.NoPen)

            shadow_color = QColor(0, 0, 0, 30) if not self._is_dark() else QColor(0, 0, 0, 60)
            shadow_rect = indicator_rect.translated(0, 1)
            painter.setBrush(shadow_color)
            painter.drawRoundedRect(shadow_rect, 8, 8)

            painter.setBrush(colors["indicator"])
            painter.drawRoundedRect(indicator_rect, 8, 8)

            font = painter.font()
            for i, label in enumerate(self._segments):
                is_selected = i == self._current_index
                if is_selected:
                    painter.setPen(colors["text"])
                    font.setBold(True)
                else:
                    painter.setPen(colors["secondary_text"])
                    font.setBold(False)
                painter.setFont(font)

                rect = QRectF(i * seg_w, 0, seg_w, h)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._segments:
            seg_w = self._segment_width()
            clicked_index = int(event.position().x() / seg_w)
            clicked_index = max(0, min(clicked_index, len(self._segments) - 1))
            self.set_current_index(clicked_index)
        super().mousePressEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._segments:
            self._update_indicator_target(self._current_index, animate=False)
