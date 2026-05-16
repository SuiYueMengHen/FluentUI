from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from qfluentwidgets import isDarkTheme


class UserCard(QFrame):
    def __init__(self, name="", bio="", posts=0, followers=0, following=0, parent=None):
        super().__init__(parent)
        self._name = name
        self._bio = bio
        self._posts = posts
        self._followers = followers
        self._following = following
        self._hover_progress = 0.0
        self._anim = QPropertyAnimation(self, b"hoverProgress")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.setFixedSize(260, 160)
        self.setMouseTracking(True)

    def get_hover_progress(self):
        return self._hover_progress

    def set_hover_progress(self, val):
        self._hover_progress = val
        self.update()

    hoverProgress = Property(float, get_hover_progress, set_hover_progress)

    def enterEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._hover_progress)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._hover_progress)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        self.update()

    def get_bio(self):
        return self._bio

    def set_bio(self, bio):
        self._bio = bio
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = isDarkTheme()
        shadow_offset = 2 + self._hover_progress * 4
        shadow_alpha = int((20 + self._hover_progress * 30))
        shadow_color = QColor(0, 0, 0, shadow_alpha)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(shadow_color)
        painter.drawRoundedRect(QRectF(shadow_offset, shadow_offset, self.width() - shadow_offset, self.height() - shadow_offset), 12, 12)
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        painter.setBrush(bg)
        border = QColor("#555555") if is_dark else QColor("#E0E0E0")
        painter.setPen(QPen(border, 1))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)
        avatar_r = 24
        avatar_cx = 40
        avatar_cy = 40
        avatar_bg = QColor("#0078D4")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(avatar_bg)
        painter.drawEllipse(QRectF(avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_r * 2, avatar_r * 2))
        initials = ""
        if self._name:
            parts = self._name.split()
            for p in parts[:2]:
                initials += p[0].upper()
        painter.setPen(QColor("#FFFFFF"))
        font = QFont()
        font.setPixelSize(16)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRectF(avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_r * 2, avatar_r * 2), Qt.AlignmentFlag.AlignCenter, initials)
        name_color = QColor("#D4D4D4") if is_dark else QColor("#1A1A1A")
        painter.setPen(name_color)
        font.setPixelSize(14)
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRectF(72, 24, 180, 20), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._name)
        bio_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
        painter.setPen(bio_color)
        font.setPixelSize(11)
        font.setWeight(QFont.Weight.Normal)
        painter.setFont(font)
        painter.drawText(QRectF(72, 44, 180, 36), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop | Qt.TextFlag.TextWordWrap, self._bio)
        stats_y = 110
        stats = [
            (str(self._posts), "Posts"),
            (str(self._followers), "Followers"),
            (str(self._following), "Following"),
        ]
        stat_w = (self.width() - 32) / 3
        for i, (val, label) in enumerate(stats):
            sx = 16 + i * stat_w
            val_color = QColor("#D4D4D4") if is_dark else QColor("#1A1A1A")
            painter.setPen(val_color)
            font.setPixelSize(14)
            font.setWeight(QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(QRectF(sx, stats_y, stat_w, 18), Qt.AlignmentFlag.AlignCenter, val)
            label_color = QColor("#9E9E9E") if is_dark else QColor("#616161")
            painter.setPen(label_color)
            font.setPixelSize(10)
            font.setWeight(QFont.Weight.Normal)
            painter.setFont(font)
            painter.drawText(QRectF(sx, stats_y + 18, stat_w, 14), Qt.AlignmentFlag.AlignCenter, label)
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
