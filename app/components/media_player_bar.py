from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class MediaPlayerBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._playing = False
        self._progress = 0.0
        self._duration = 240
        self._current_time = 0
        self._volume = 0.7
        self._press_scale = 1.0
        self._hovered_btn = 0
        self._dragging = False
        self.setFixedSize(400, 56)
        self.setMouseTracking(True)

        self._press_anim = QPropertyAnimation(self, b"pressScale")
        self._press_anim.setDuration(150)
        self._press_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def get_press_scale(self):
        return self._press_scale

    def set_press_scale(self, val):
        self._press_scale = val
        self.update()

    pressScale = Property(float, get_press_scale, set_press_scale)

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
            self.update()

    def _skip_back_rect(self):
        return QRectF(100, 12, 32, 32)

    def _play_rect(self):
        return QRectF(140, 8, 40, 40)

    def _skip_forward_rect(self):
        return QRectF(188, 12, 32, 32)

    def _progress_bar_rect(self):
        return QRectF(16, 40, 368, 4)

    def _volume_rect(self):
        return QRectF(340, 14, 24, 24)

    def mousePressEvent(self, event):
        pos = event.position()
        if self._play_rect().contains(pos):
            self._playing = not self._playing
            if self._playing:
                self._timer.start(1000)
            else:
                self._timer.stop()
            self._press_anim.setStartValue(0.9)
            self._press_anim.setEndValue(1.0)
            self._press_anim.start()
        elif self._skip_back_rect().contains(pos):
            self._current_time = max(0, self._current_time - 10)
            self._progress = self._current_time / max(self._duration, 1)
        elif self._skip_forward_rect().contains(pos):
            self._current_time = min(self._duration, self._current_time + 10)
            self._progress = self._current_time / max(self._duration, 1)
        elif self._progress_bar_rect().adjusted(0, -6, 0, 6).contains(pos):
            self._dragging = True
            self._update_progress(pos.x())
        self.update()

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_btn = 0
        if self._skip_back_rect().contains(pos):
            self._hovered_btn = 1
        elif self._play_rect().contains(pos):
            self._hovered_btn = 2
        elif self._skip_forward_rect().contains(pos):
            self._hovered_btn = 3
        if self._dragging:
            self._update_progress(pos.x())
        self.update()

    def mouseReleaseEvent(self, event):
        self._dragging = False

    def _update_progress(self, x):
        bar = self._progress_bar_rect()
        self._progress = max(0.0, min(1.0, (x - bar.x()) / bar.width()))
        self._current_time = int(self._progress * self._duration)
        self.update()

    def _format_time(self, s):
        m = int(s) // 60
        sec = int(s) % 60
        return f"{m}:{sec:02d}"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#1E1E1E") if is_dark else QColor("#FFFFFF")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if is_dark else QColor("#666666")
        accent = QColor("#0078D4")
        track_bg = QColor("#3D3D3D") if is_dark else QColor("#E5E5E5")
        btn_hover = QColor("#3D3D3D") if is_dark else QColor("#E8E8E8")

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect(), 8, 8)

        skip_back = self._skip_back_rect()
        if self._hovered_btn == 1:
            painter.setBrush(btn_hover)
            painter.drawRoundedRect(skip_back, 6, 6)
        icon_sb = FIF.SKIP_BACK.icon()
        painter.drawPixmap(int(skip_back.x() + 6), int(skip_back.y() + 6), icon_sb.pixmap(20, 20))

        play = self._play_rect()
        painter.save()
        cx = play.center().x()
        cy = play.center().y()
        painter.translate(cx, cy)
        painter.scale(self._press_scale, self._press_scale)
        painter.translate(-cx, -cy)
        painter.setBrush(accent if self._hovered_btn == 2 else accent)
        painter.drawRoundedRect(play, 8, 8)
        play_icon = FIF.PAUSE if self._playing else FIF.PLAY
        icon_p = play_icon.icon()
        painter.drawPixmap(int(play.x() + 10), int(play.y() + 8), icon_p.pixmap(24, 24))
        painter.restore()

        skip_fwd = self._skip_forward_rect()
        if self._hovered_btn == 3:
            painter.setBrush(btn_hover)
            painter.drawRoundedRect(skip_fwd, 6, 6)
        icon_sf = FIF.SKIP_FORWARD.icon()
        painter.drawPixmap(int(skip_fwd.x() + 6), int(skip_fwd.y() + 6), icon_sf.pixmap(20, 20))

        bar = self._progress_bar_rect()
        painter.setBrush(track_bg)
        painter.drawRoundedRect(bar, 2, 2)
        fill_w = bar.width() * self._progress
        painter.setBrush(accent)
        painter.drawRoundedRect(QRectF(bar.x(), bar.y(), fill_w, bar.height()), 2, 2)

        vol = self._volume_rect()
        icon_v = FIF.VOLUME.icon()
        painter.drawPixmap(int(vol.x() + 3), int(vol.y() + 3), icon_v.pixmap(18, 18))

        time_str = f"{self._format_time(self._current_time)}/{self._format_time(self._duration)}"
        painter.setPen(sub_color)
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(QRectF(280, 14, 56, 20), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, time_str)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self._playing:
            self._timer.start(1000)

    def hideEvent(self, event):
        if self._timer.isActive():
            self._timer.stop()
        super().hideEvent(event)

    def refresh_theme(self):
        self.update()
        self.repaint()
