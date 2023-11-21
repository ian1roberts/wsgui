from PySide6.QtGui import QPixmap, QPainterPath, QPen, QImage
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QGraphicsPathItem
)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np

FONT_FILE = Path( "c:") / "Windows" / "Fonts" / "arial.ttf"

class MyQGPixmapItem(QGraphicsPixmapItem):
    def __init__(self, img, i, n, alpha, center, radius):
        super().__init__(img)
        self.idx = i
        self.alpha = alpha
        self.half_width = self.boundingRect().width() / 2
        self.half_height = self.boundingRect().height() / 2
        self.center_x = center.x()
        self.center_y = center.y()
        self.radius = radius
        self.angle = 2 * math.pi * i / n
        self.hit = False

    def calc_position(self,  r = False, offset = False):
        if not r:
            r = self.radius
        x = self.center_x + r * math.cos(self.angle)
        if not offset:
            x -= self.half_width
        y = self.center_y + r * math.sin(self.angle)
        if not offset:
            y -= self.half_height
        if not offset:
            self.setPos(x, y)
        else:
            self.offset_xy = QPointF(x, y)

class LetterArea(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.center = QPointF(50, 50)
        self.radius = 80
        self.last_path = False
        self.get_letters()

    def create_letter_img(self, char, fnt_file = FONT_FILE):
        fnt = ImageFont.truetype(str(fnt_file), size = 24)
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
        letters = [MyQGPixmapItem(
                self.letters[alpha], i, len(word), alpha, self.center,
                self.radius) for i, alpha in enumerate(word)]

        for letter in letters:
            letter.calc_position()
            letter.calc_position(r = self.radius - 15,
                                 offset = True)
            self.scene.addItem(letter)

        path = QPainterPath()
        path.moveTo(letters[0].offset_xy)
        for letter in letters:
            path.lineTo(letter.offset_xy)
        path.closeSubpath()
        self.scene.addPath(path, QPen(Qt.red, 3))
        self.wheel = letters

    def word_path(self, word):
        tmp_letters = self.wheel.copy()
        selected = list()
        for w in word:
            for x in tmp_letters:
                if (x.alpha == w) and (not x.hit):
                    x.hit = True
                    selected.append(x)
                    break
        
        path = QPainterPath()
        path.moveTo(selected[0].offset_xy)
        for letter in selected[1:]:
            path.lineTo(letter.offset_xy)
        path_item = QGraphicsPathItem(path)
        path_item.setPen(QPen(Qt.blue, 3))
        self.scene.addItem(path_item)
        for x in self.wheel:
            x.hit = False
        self.last_path = path_item

