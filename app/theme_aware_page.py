from PySide6.QtWidgets import QGroupBox, QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer
from qfluentwidgets import isDarkTheme, ScrollArea, Theme, setTheme


class ThemeAwarePage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_groups = []
        self._theme_labels = []
        self._theme_title_labels = []
        self._theme_section_labels = []
        self._theme_custom_widgets = []
        self._paused_timers = {}
        self._needs_theme_refresh = False
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: transparent; }")

    def _track_group(self, group: QGroupBox):
        self._theme_groups.append(group)
        group.setStyleSheet(self._current_group_style())
        return group

    def _track_label(self, label: QLabel, role="secondary"):
        self._theme_labels.append((label, role))
        label.setStyleSheet(self._label_style(role) + "background: transparent;")
        return label

    def _track_title(self, label: QLabel):
        self._theme_title_labels.append(label)
        color = "#1A1A1A" if not isDarkTheme() else "#FFFFFF"
        label.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {color}; background: transparent;")
        return label

    def _track_section_title(self, label: QLabel):
        self._theme_section_labels.append(label)
        color = "#1A1A1A" if not isDarkTheme() else "#FFFFFF"
        label.setStyleSheet(f"font-size: 20px; font-weight: 600; color: {color}; background: transparent;")
        return label

    def _track_custom_widget(self, widget):
        self._theme_custom_widgets.append(widget)
        return widget

    def _current_group_style(self):
        if isDarkTheme():
            return """
                QGroupBox {
                    font-size: 16px; font-weight: 600;
                    color: #FFFFFF;
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px;
                    margin-top: 16px;
                    padding: 20px;
                    padding-top: 36px;
                    background-color: rgba(255,255,255,0.04);
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 20px;
                    padding: 0 8px;
                    color: #FFFFFF;
                }
            """
        else:
            return """
                QGroupBox {
                    font-size: 16px; font-weight: 600;
                    color: #1A1A1A;
                    border: 1px solid rgba(0,0,0,0.1);
                    border-radius: 12px;
                    margin-top: 16px;
                    padding: 20px;
                    padding-top: 36px;
                    background-color: rgba(255,255,255,0.7);
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 20px;
                    padding: 0 8px;
                    color: #1A1A1A;
                }
            """

    def _label_style(self, role):
        if role == "secondary":
            color = "#9E9E9E" if isDarkTheme() else "#616161"
            return f"color: {color}; "
        return ""

    def refresh_theme(self):
        is_dark = isDarkTheme()
        text_color = "#FFFFFF" if is_dark else "#1A1A1A"
        bg_color = "#202020" if is_dark else "#F3F3F3"
        secondary_color = "#9E9E9E" if is_dark else "#616161"

        for group in self._theme_groups:
            group.setStyleSheet(self._current_group_style())

        for label, role in self._theme_labels:
            new_style = self._label_style(role) + "background: transparent;"
            label.setStyleSheet(new_style)

        for label in self._theme_title_labels:
            label.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {text_color}; background: transparent;")

        for label in self._theme_section_labels:
            label.setStyleSheet(f"font-size: 20px; font-weight: 600; color: {text_color}; background: transparent;")

        container = self.widget()
        if container:
            container.setStyleSheet(f"background-color: {bg_color};")

        for widget in self._theme_custom_widgets:
            if hasattr(widget, 'refresh_theme'):
                widget.refresh_theme()
            widget.update()

        viewport = self.viewport()
        if viewport:
            viewport.setStyleSheet(f"background-color: {bg_color};")

        self.update()

    def _stop_child_animations(self, widget):
        self._paused_timers.clear()
        for anim in widget.findChildren(QPropertyAnimation):
            if anim.state() == QPropertyAnimation.State.Running:
                anim.pause()
        for timer in widget.findChildren(QTimer):
            if timer.isActive():
                self._paused_timers[id(timer)] = timer
                timer.stop()

    def _start_child_animations(self, widget):
        for anim in widget.findChildren(QPropertyAnimation):
            if anim.state() == QPropertyAnimation.State.Paused:
                anim.resume()
        for timer_id, timer in self._paused_timers.items():
            try:
                timer.start()
            except RuntimeError:
                pass
        self._paused_timers.clear()

    def hideEvent(self, event):
        container = self.widget()
        if container:
            self._stop_child_animations(container)
        super().hideEvent(event)

    def mark_theme_stale(self):
        self._needs_theme_refresh = True

    def showEvent(self, event):
        super().showEvent(event)
        container = self.widget()
        if container:
            self._start_child_animations(container)
        if self._needs_theme_refresh:
            self._needs_theme_refresh = False
            self.refresh_theme()
