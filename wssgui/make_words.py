from PySide6.QtGui import QPixmap, QPainterPath, QPen, QImage
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QGraphicsPathItem
)

from wssgui.letter_wheel import LetterArea, MyQGPixmapItem

class MakeWordArea(LetterArea):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.word = ""

    @property
    def new_x(self):
        return self.x() + (len(self.word) * 20)

    @property
    def new_y(self):
        return self.y() + self.height() / 2

    def add_letter(self, alpha):
        letter = MyQGPixmapItem(self.letters[alpha],
                1, 1, alpha, self.center,
                self.radius, self.selected_alpha)
        letter.setPos(self.new_x, self.new_y)
        print(letter)
        self.scene.addItem(letter)
        self.word += alpha
        self.update()
