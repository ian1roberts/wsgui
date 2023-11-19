from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
    QTabWidget
)

class WordArea(QTabWidget):

    def __init__(self) -> None:
        super().__init__()
        self.create_tabs()

    def create_tabs(self):
        self.layout = QGridLayout()
        for i in range(2, 9):
            cur_tab = QLabel(f"{i} letter words.")
            self.addTab(cur_tab, f"{i} letter words.")
        self.layout.addWidget(self, 0, 0)
