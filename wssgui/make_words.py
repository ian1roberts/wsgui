from wssgui.letter_wheel import LetterArea, MyQGPixmapItem


class MakeWordArea(LetterArea):
    def __init__(self) -> None:
        super().__init__()
        self.word = ""

    @property
    def new_x(self):
        return self.x() + (len(self.word) * 25)

    @property
    def new_y(self):
        return self.y() + self.height() / 2

    def add_letter(self, alpha):
        letter = MyQGPixmapItem(
            self.letters[alpha], 1, 1, alpha, self.center, self.radius
        )
        letter.setPos(self.new_x, self.new_y)
        self.scene.addItem(letter)
        self.word += alpha
       # self.update()
