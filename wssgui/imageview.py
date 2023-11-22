from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap

class ImageArea(QWidget):

    def __init__(self, size = 200, scale = 2.17) -> None:
        super().__init__()
        self.container = QLabel("")
        self.container.setFixedHeight(size * scale)
        self.container.setFixedWidth(size)

    def load_image(self, file_name):
        self.file_name = file_name
        pixmap = QPixmap(file_name)
        self.container.setPixmap(pixmap)
        self.container.setScaledContents(True)
        self.container.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored)
