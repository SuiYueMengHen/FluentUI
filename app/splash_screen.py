from PySide6.QtWidgets import QSplashScreen, QVBoxLayout, QWidget, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap, QLinearGradient


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setFixedSize(520, 320)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._progress = 0
        self._target_progress = 0

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_progress)
        self._timer.start(30)

    def _update_progress(self):
        if self._progress < self._target_progress:
            self._progress += 1
            self.repaint()
        if self._progress >= 100:
            self._timer.stop()

    def set_progress(self, value: int):
        self._target_progress = min(value, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        from qfluentwidgets import isDarkTheme
        is_dark = isDarkTheme()

        bg_color = QColor("#202020") if is_dark else QColor("#FAFAFA")
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 12, 12)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#0078D4"))
        gradient.setColorAt(1, QColor("#0067C0"))
        painter.setBrush(gradient)
        painter.drawRoundedRect(0, 0, self.width(), 6, 3, 3)

        title_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        painter.setPen(title_color)
        font = QFont("Segoe UI Variable, Segoe UI", 28, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(0, 40, 0, 0), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, "FluentUI Gallery")

        subtitle_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
        painter.setPen(subtitle_color)
        font = QFont("Segoe UI Variable, Segoe UI", 13)
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(0, 100, 0, 0), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, "Modern Desktop Component Showcase")

        bar_x = 60
        bar_y = 240
        bar_w = self.width() - 120
        bar_h = 6

        bar_bg = QColor("#3D3D3D") if is_dark else QColor("#E5E5E5")
        painter.setBrush(bar_bg)
        painter.drawRoundedRect(bar_x, bar_y, bar_w, bar_h, 3, 3)

        progress_w = int(bar_w * self._progress / 100)
        if progress_w > 0:
            bar_gradient = QLinearGradient(bar_x, 0, bar_x + progress_w, 0)
            bar_gradient.setColorAt(0, QColor("#0078D4"))
            bar_gradient.setColorAt(1, QColor("#60CDFF"))
            painter.setBrush(bar_gradient)
            painter.drawRoundedRect(bar_x, bar_y, progress_w, bar_h, 3, 3)

        percent_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
        painter.setPen(percent_color)
        font = QFont("Segoe UI Variable, Segoe UI", 11)
        painter.setFont(font)
        painter.drawText(
            self.rect().adjusted(0, 260, 0, 0),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
            f"Loading... {self._progress}%",
        )

        painter.end()

    def fade_out(self):
        self.close()
