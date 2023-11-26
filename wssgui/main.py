import sys

from PySide6.QtWidgets import QApplication

from wssgui.main_window import MainWindow


def main(xargs):
    app = QApplication(xargs)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    xargs = sys.argv
    main(xargs)
