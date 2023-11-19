from PySide6.QtGui import QPixmap, QPainterPath, QPen, QImage
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem
)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np

FONT_FILE = Path( "c:") / "Windows" / "Fonts" / "arial.ttf"


class LetterArea(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.center = QPointF(50, 50)
        self.radius = 50
        self.get_letters()

    def create_letter_img(self, char, fnt_file = FONT_FILE):
        fnt = ImageFont.truetype(str(fnt_file), size = 32)
        l, t, r, b = fnt.getbbox(char)
        h = b - t
        w = r - l
        img_w, img_h = w + 10, h + 10
        img = Image.new("L", (img_w, img_h), color='white')
        d = ImageDraw.Draw(img)
        d.text((img_w / 2, img_h /2),
            char, font = fnt, fill = 0, anchor = "mm")
        np_image = np.array(img)
        qimage = QImage(np_image.data, np_image.shape[1],
                        np_image.shape[0], np_image.strides[0],
                        QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimage)

    def get_letters(self):
        self.letters = {alpha: self.create_letter_img(alpha) for
                        alpha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

    def make_word(self, word):
        def _get_position(l):
            start_pos_x = l.x()
            start_pos_y = l.y()
            start_height =  l.boundingRect().height()
            start_width =  l.boundingRect().width()
            x = start_pos_x + (start_width / 2)
            y = start_pos_y + (start_height / 2)
            return(QPointF(x, y))

        letters = [QGraphicsPixmapItem(self.letters[alpha])
                   for alpha in word]
        for i, letter in enumerate(letters):
            angle = 2 * math.pi * i / len(word)
            x = (self.center.x() + self.radius * math.cos(angle) -
                 letter.boundingRect().width() / 2)
            y = (self.center.y() + self.radius * math.sin(angle) -
                 letter.boundingRect().height() / 2)
            letter.setPos(x, y)
            self.scene.addItem(letter)

        path = QPainterPath()
        path.moveTo(_get_position(letters[0]))
        for letter in letters:
            path.lineTo(_get_position(letter))
        path.closeSubpath()
        self.scene.addPath(path, QPen(Qt.red, 3))
