import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def create_application():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("FluentUI Gallery")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FluentUI")

    font = QFont("Segoe UI Variable, Segoe UI, Microsoft YaHei UI", 14)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)

    return app
