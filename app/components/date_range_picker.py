from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, Signal, QDate
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
from PySide6.QtCore import QLocale
from qfluentwidgets import FluentIcon as FIF, isDarkTheme


class DateRangePicker(QWidget):
    rangeSelected = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._start_date = None
        self._end_date = None
        self._hovered_day = (-1, -1, -1)
        self._current_month = QDate.currentDate().month()
        self._current_year = QDate.currentDate().year()
        self._expanded = False
        self._expand_progress = 0.0
        self.setFixedSize(320, 36)
        self.setMouseTracking(True)

        self._expand_anim = QPropertyAnimation(self, b"expandProgress")
        self._expand_anim.setDuration(200)
        self._expand_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._expand_anim.valueChanged.connect(self._on_expand_changed)

    def get_expand_progress(self):
        return self._expand_progress

    def set_expand_progress(self, val):
        self._expand_progress = val
        self.update()

    expandProgress = Property(float, get_expand_progress, set_expand_progress)

    def _is_dark(self):
        return isDarkTheme()

    def _on_expand_changed(self, val):
        h = 36 + int(280 * val)
        self.setFixedHeight(h)

    def _trigger_rect(self):
        return QRectF(0, 0, self.width(), 36)

    def _month_grid_origin(self, month_offset):
        x = 8 + month_offset * 158
        y = 44
        return x, y

    def _day_rect(self, month_offset, row, col):
        ox, oy = self._month_grid_origin(month_offset)
        x = ox + col * 22
        y = oy + 20 + row * 22
        return QRectF(x, y, 20, 20)

    def _toggle_expand(self):
        self._expanded = not self._expanded
        if self._expanded:
            self._expand_anim.setStartValue(0.0)
            self._expand_anim.setEndValue(1.0)
        else:
            self._expand_anim.setStartValue(1.0)
            self._expand_anim.setEndValue(0.0)
        self._expand_anim.start()

    def _days_in_month(self, year, month):
        return QDate(year, month, 1).daysInMonth()

    def _first_day_offset(self, year, month):
        day = QDate(year, month, 1).dayOfWeek()
        return day - 1

    def mousePressEvent(self, event):
        pos = event.position()
        if self._trigger_rect().contains(pos):
            self._toggle_expand()
            return
        if self._expanded:
            for offset in range(2):
                month = self._current_month + offset
                year = self._current_year
                if month > 12:
                    month -= 12
                    year += 1
                days = self._days_in_month(year, month)
                first_offset = self._first_day_offset(year, month)
                for d in range(1, days + 1):
                    idx = first_offset + d - 1
                    row = idx // 7
                    col = idx % 7
                    rect = self._day_rect(offset, row, col)
                    if rect.contains(pos):
                        clicked = QDate(year, month, d)
                        if self._start_date is None or (self._start_date and self._end_date):
                            self._start_date = clicked
                            self._end_date = None
                        elif clicked < self._start_date:
                            self._start_date = clicked
                        else:
                            self._end_date = clicked
                            self.rangeSelected.emit(
                                self._start_date.toString("yyyy-MM-dd"),
                                self._end_date.toString("yyyy-MM-dd")
                            )
                        self.update()
                        return

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_day = (-1, -1, -1)
        if self._expanded:
            for offset in range(2):
                month = self._current_month + offset
                year = self._current_year
                if month > 12:
                    month -= 12
                    year += 1
                days = self._days_in_month(year, month)
                first_offset = self._first_day_offset(year, month)
                for d in range(1, days + 1):
                    idx = first_offset + d - 1
                    row = idx // 7
                    col = idx % 7
                    rect = self._day_rect(offset, row, col)
                    if rect.contains(pos):
                        self._hovered_day = (offset, row, col)
                        break
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        is_dark = self._is_dark()
        bg = QColor("#2D2D2D") if is_dark else QColor("#FFFFFF")
        border_color = QColor("#555555") if is_dark else QColor("#CCCCCC")
        text_color = QColor("#FFFFFF") if is_dark else QColor("#1A1A1A")
        sub_color = QColor("#AAAAAA") if is_dark else QColor("#666666")
        accent = QColor("#0078D4")
        hover_bg = QColor("#3D3D3D") if is_dark else QColor("#F0F0F0")
        range_bg = QColor(0, 120, 212, 40)
        day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        trigger = self._trigger_rect()
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(trigger, 6, 6)

        label = "Select date range..."
        if self._start_date and self._end_date:
            label = f"{self._start_date.toString('MM/dd')} - {self._end_date.toString('MM/dd')}"
        elif self._start_date:
            label = f"From {self._start_date.toString('MM/dd')}..."

        painter.setPen(text_color if self._start_date else sub_color)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(QRectF(10, 0, trigger.width() - 30, 36),
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)

        cal_icon = FIF.CALENDAR.icon()
        painter.drawPixmap(int(trigger.right() - 26), 8, cal_icon.pixmap(20, 20))

        if self._expand_progress > 0:
            painter.setOpacity(self._expand_progress)

            panel_rect = QRectF(0, 36, self.width(), 280)
            painter.setPen(QPen(border_color, 1))
            painter.setBrush(bg)
            painter.drawRect(panel_rect)

            for offset in range(2):
                month = self._current_month + offset
                year = self._current_year
                if month > 12:
                    month -= 12
                    year += 1

                ox, oy = self._month_grid_origin(offset)
                painter.setPen(text_color)
                font.setPointSize(10)
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(QRectF(ox, oy - 16, 140, 16),
                               Qt.AlignmentFlag.AlignCenter, f"{QLocale().monthName(month, QLocale.FormatType.LongFormat)} {year}")
                font.setBold(False)

                font.setPointSize(7)
                painter.setFont(font)
                painter.setPen(sub_color)
                for c, name in enumerate(day_names):
                    painter.drawText(QRectF(ox + c * 22, oy, 20, 16),
                                   Qt.AlignmentFlag.AlignCenter, name)

                days = self._days_in_month(year, month)
                first_offset = self._first_day_offset(year, month)

                font.setPointSize(9)
                painter.setFont(font)
                for d in range(1, days + 1):
                    idx = first_offset + d - 1
                    row = idx // 7
                    col = idx % 7
                    rect = self._day_rect(offset, row, col)
                    date = QDate(year, month, d)

                    in_range = False
                    is_start = self._start_date and date == self._start_date
                    is_end = self._end_date and date == self._end_date
                    if self._start_date and self._end_date:
                        in_range = self._start_date <= date <= self._end_date

                    if in_range:
                        painter.setPen(Qt.PenStyle.NoPen)
                        painter.setBrush(range_bg)
                        painter.drawRect(rect)

                    if is_start or is_end:
                        painter.setPen(Qt.PenStyle.NoPen)
                        painter.setBrush(accent)
                        painter.drawEllipse(rect.adjusted(2, 2, -2, -2))
                        painter.setPen(QColor("#FFFFFF"))
                    elif self._hovered_day == (offset, row, col):
                        painter.setPen(Qt.PenStyle.NoPen)
                        painter.setBrush(hover_bg)
                        painter.drawEllipse(rect.adjusted(2, 2, -2, -2))
                        painter.setPen(text_color)
                    else:
                        painter.setPen(text_color)

                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(d))

            painter.setOpacity(1.0)

        painter.end()

    def refresh_theme(self):
        self.update()
        self.repaint()
