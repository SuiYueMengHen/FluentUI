import sys
from PySide6.QtCore import QTimer
from app.application import create_application
from app.splash_screen import SplashScreen
from app.main_window import MainWindow


def main():
    app = create_application()

    splash = SplashScreen()
    splash.show()

    splash.set_progress(20)

    def load_step_1():
        splash.set_progress(50)

    def load_step_2():
        splash.set_progress(80)

    def load_step_3():
        splash.set_progress(100)

    def show_main():
        splash.fade_out()
        window = MainWindow()
        window.show()

    QTimer.singleShot(300, load_step_1)
    QTimer.singleShot(700, load_step_2)
    QTimer.singleShot(1100, load_step_3)
    QTimer.singleShot(1800, show_main)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
