# from typing import Optional
# from PySide6.QtCore import Qt, QRect
# from PySide6.QtGui import QBrush, QColor, QPainter, QFont
from PySide6.QtWidgets import QWidget

class ImageArea(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(300, 300)
