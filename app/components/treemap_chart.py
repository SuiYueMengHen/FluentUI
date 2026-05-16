from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from qfluentwidgets import isDarkTheme


class TreemapChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._expand_progress = 0.0
        self._rects = []
        self.setMinimumSize(200, 150)

        self._anim = QPropertyAnimation(self, b"_expand_progress_prop")
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._first_show = True

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress(self, val):
        self._expand_progress = val
        self.update()

    _expand_progress_prop = Property(float, get_expand_progress, set_expand_progress)

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self._anim.start()

    def hideEvent(self, event):
        if self._anim.state() == QPropertyAnimation.State.Running:
            self._anim.pause()
        super().hideEvent(event)

    def _is_dark(self):
        return isDarkTheme()

    def refresh_theme(self):
        self.update()
        self.repaint()

    def _squarify(self, data, x, y, w, h):
        if not data or w <= 0 or h <= 0:
            return []

        total = sum(d["value"] for d in data)
        if total == 0:
            return []

        result = []
        remaining = list(data)
        cx, cy, cw, ch = x, y, w, h

        while remaining:
            if cw <= 0 or ch <= 0:
                break

            is_wider = cw >= ch
            side = ch if is_wider else cw

            row = []
            row_area = 0
            for item in remaining:
                test_row = row + [item]
                test_area = row_area + item["value"] / total * cw * ch
                if not row:
                    row.append(item)
                    row_area = test_area
                    continue

                row_side = test_area / side if side > 0 else 0
                worst = self._worst_ratio(row, test_area, side)
                prev_worst = self._worst_ratio(row, row_area, side)
                if worst <= prev_worst:
                    row.append(item)
                    row_area = test_area
                else:
                    break

            if not row:
                break

            row_total = sum(d["value"] for d in row)
            row_fraction = row_total / total if total > 0 else 0

            if is_wider:
                row_w = cw * row_fraction
                offset = 0
                for item in row:
                    item_fraction = item["value"] / row_total if row_total > 0 else 0
                    item_h = ch * item_fraction
                    result.append({
                        "name": item["name"],
                        "color": item.get("color", "#0078D4"),
                        "rect": QRectF(cx, cy + offset, row_w, item_h)
                    })
                    offset += item_h
                cx += row_w
                cw -= row_w
            else:
                row_h = ch * row_fraction
                offset = 0
                for item in row:
                    item_fraction = item["value"] / row_total if row_total > 0 else 0
                    item_w = cw * item_fraction
                    result.append({
                        "name": item["name"],
                        "color": item.get("color", "#0078D4"),
                        "rect": QRectF(cx + offset, cy, item_w, row_h)
                    })
                    offset += item_w
                cy += row_h
                ch -= row_h

            for item in row:
                remaining.remove(item)
            total = sum(d["value"] for d in remaining) if remaining else 0
            if total == 0:
                break

        return result

    def _worst_ratio(self, row, area, side):
        if not row or area <= 0 or side <= 0:
            return float('inf')
        row_total = sum(d["value"] for d in row)
        worst = 0
        for item in row:
            item_area = item["value"] / row_total * area if row_total > 0 else 0
            if item_area <= 0:
                continue
            other_side = item_area / side if side > 0 else 0
            ratio = max(side / other_side, other_side / side) if other_side > 0 else float('inf')
            worst = max(worst, ratio)
        return worst

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._is_dark()
        label_color = QColor("#FFFFFF")
        value_color = QColor("#FFFFFF")

        w = self.width()
        h = self.height()
        padding = 4

        if not self._data:
            painter.end()
            return

        sorted_data = sorted(self._data, key=lambda d: d["value"], reverse=True)
        rects = self._squarify(sorted_data, padding, padding, w - padding * 2, h - padding * 2)

        font = QFont()
        painter.setFont(font)

        cx = w / 2
        cy = h / 2

        for item in rects:
            target_rect = item["rect"]
            color = QColor(item["color"])

            anim_rect = QRectF(
                cx + (target_rect.x() - cx) * self._expand_progress,
                cy + (target_rect.y() - cy) * self._expand_progress,
                target_rect.width() * self._expand_progress,
                target_rect.height() * self._expand_progress
            )

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(anim_rect, 4, 4)

            border_color = QColor(color)
            border_color.setAlpha(40)
            painter.setBrush(QBrush(border_color))
            painter.drawRoundedRect(anim_rect, 4, 4)

            if self._expand_progress > 0.7 and anim_rect.width() > 40 and anim_rect.height() > 24:
                brightness = color.red() * 0.299 + color.green() * 0.587 + color.blue() * 0.114
                text_c = QColor("#FFFFFF") if brightness < 128 else QColor("#1A1A1A")

                painter.setPen(text_c)
                font.setPixelSize(min(13, int(anim_rect.height() * 0.3)))
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(anim_rect.adjusted(6, 4, -6, -anim_rect.height() * 0.4), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, item["name"])

                font.setPixelSize(min(11, int(anim_rect.height() * 0.22)))
                font.setBold(False)
                painter.setFont(font)
                painter.drawText(anim_rect.adjusted(6, anim_rect.height() * 0.5, -6, -4), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom, f"{item.get('value', 0):.0f}")

        painter.end()
