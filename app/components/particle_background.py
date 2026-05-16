import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class ParticleBackground(QWidget):
    def __init__(self, particle_count=50, color="#0078D4", parent=None):
        super().__init__(parent)
        self._particle_count = particle_count
        self._color = color
        self._particles = []
        self._init_particles()
        self.setMinimumSize(300, 200)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_particles)

    def showEvent(self, event):
        super().showEvent(event)
        self._timer.start(33)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def _init_particles(self):
        import random
        self._particles = []
        for _ in range(self._particle_count):
            self._particles.append({
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "vx": random.uniform(-0.002, 0.002),
                "vy": random.uniform(-0.002, 0.002),
                "opacity": random.uniform(0.3, 0.8),
                "size": random.uniform(2, 5),
            })

    def _update_particles(self):
        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["x"] < 0 or p["x"] > 1:
                p["vx"] *= -1
            if p["y"] < 0 or p["y"] > 1:
                p["vy"] *= -1
            p["x"] = max(0, min(1, p["x"]))
            p["y"] = max(0, min(1, p["y"]))
        self.update()

    def set_color(self, color):
        self._color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        dark = isDarkTheme()
        bg = QColor("#1A1A1A") if dark else QColor("#F5F5F5")
        particle_color = QColor(self._color)
        if dark:
            particle_color = particle_color.lighter(120)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRect(self.rect())
        w = self.width()
        h = self.height()
        positions = []
        for p in self._particles:
            px = p["x"] * w
            py = p["y"] * h
            positions.append((px, py))
            c = QColor(particle_color)
            c.setAlpha(int(255 * p["opacity"]))
            painter.setBrush(c)
            r = p["size"]
            painter.drawEllipse(QRectF(px - r, py - r, r * 2, r * 2))
        line_color = QColor(particle_color)
        connect_dist = 100
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < connect_dist:
                    alpha = int(60 * (1 - dist / connect_dist))
                    line_color.setAlpha(alpha)
                    painter.setPen(QPen(line_color, 1))
                    painter.drawLine(QPointF(positions[i][0], positions[i][1]), QPointF(positions[j][0], positions[j][1]))
        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
