from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme, FluentIcon


class AudioPlayer(QWidget):
    def __init__(self, title="", duration=180, parent=None):
        super().__init__(parent)
        self._title = title
        self._duration = duration
        self._current_time = 0
        self._playing = False
        self._fade_progress = 0.0
        self._progress = 0.0
        self._dragging = False
        self.setFixedSize(320, 64)
        self.setMouseTracking(True)

        self._fade_anim = QPropertyAnimation(self, b"fadeProgress")
        self._fade_anim.setDuration(150)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._first_show = True

    def get_fade_progress(self):
        return self._fade_progress

    def set_fade_progress(self, val):
        self._fade_progress = val
        self.update()

    fadeProgress = Property(float, get_fade_progress, set_fade_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _tick(self):
        if self._playing and self._current_time < self._duration:
            self._current_time += 1
            self._progress = self._current_time / max(self._duration, 1)
            self.update()
        else:
            self._timer.stop()
            self._playing = False
            self._fade_anim.setStartValue(1.0)
            self._fade_anim.setEndValue(0.0)
            self._fade_anim.start()

    def _toggle_play(self):
        self._playing = not self._playing
        if self._playing:
            self._timer.start(1000)
            self._fade_anim.setStartValue(0.0)
            self._fade_anim.setEndValue(1.0)
        else:
            self._timer.stop()
            self._fade_anim.setStartValue(1.0)
            self._fade_anim.setEndValue(0.0)
        self._fade_anim.start()

    def _progress_bar_rect(self):
        return QRectF(52, 38, 200, 6)

    def _play_icon_rect(self):
        return QRectF(8, 12, 36, 36)

    def _volume_icon_rect(self):
        return QRectF(268, 20, 24, 24)

    def mousePressEvent(self, event):
        pos = event.position()
        if self._play_icon_rect().contains(pos):
            self._toggle_play()
        elif self._progress_bar_rect().contains(pos):
            self._dragging = True
            self._update_progress_from_pos(pos.x())
        elif self._volume_icon_rect().contains(pos):
            pass

    def mouseMoveEvent(self, event):
        if self._dragging:
            self._update_progress_from_pos(event.position().x())

    def mouseReleaseEvent(self, event):
        self._dragging = False

    def _update_progress_from_pos(self, x):
        bar = self._progress_bar_rect()
        ratio = max(0.0, min(1.0, (x - bar.x()) / bar.width()))
        self._progress = ratio
        self._current_time = int(ratio * self._duration)
        self.update()

    def _format_time(self, seconds):
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m}:{s:02d}"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if is_dark else QColor("#666666")
        accent = QColor("#0078D4")
        track_bg = QColor("#3D3D3D") if is_dark else QColor("#E5E5E5")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        play_icon = FIF.PAUSE if self._playing else FIF.PLAY
        icon = play_icon.icon()
        pixmap = icon.pixmap(20, 20)
        pr = self._play_icon_rect()
        painter.drawPixmap(int(pr.x() + 8), int(pr.y() + 8), pixmap)

        painter.setPen(text_color)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(QRectF(52, 8, 200, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._title)

        bar = self._progress_bar_rect()
        painter.setBrush(track_bg)
        painter.drawRoundedRect(bar, 3, 3)

        fill_w = bar.width() * self._progress
        fill_rect = QRectF(bar.x(), bar.y(), fill_w, bar.height())
        painter.setBrush(accent)
        painter.drawRoundedRect(fill_rect, 3, 3)

        handle_x = bar.x() + fill_w
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(QRectF(handle_x - 5, bar.y() - 2, 10, 10))

        time_str = f"{self._format_time(self._current_time)} / {self._format_time(self._duration)}"
        painter.setPen(sub_color)
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(QRectF(260, 36, 56, 16), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, time_str)

        vol_icon = FIF.VOLUME.icon()
        vol_pixmap = vol_icon.pixmap(18, 18)
        vr = self._volume_icon_rect()
        painter.drawPixmap(int(vr.x() + 3), int(vr.y() + 3), vol_pixmap)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            return
        if self._playing:
            self._timer.start(1000)

    def hideEvent(self, event):
        if self._timer.isActive():
            self._timer.stop()
        super().hideEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
