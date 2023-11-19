from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QFrame,
    QRadioButton
)
from PySide6.QtCore import Qt

class WordArea(QTabWidget):

    def __init__(self) -> None:
        super().__init__()

    def create_tabs(self, all_words):
        for k, words in all_words.items():
            cur_tab = QFrame()
            cur_layout = QVBoxLayout()
            cur_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            for word in words:
                row = QHBoxLayout()
                word_button = QRadioButton()
                word_label = QLabel(word)
                row.addWidget(word_button)
                row.addWidget(word_label)
                cur_layout.addLayout(row)

            cur_tab.setLayout(cur_layout)
            self.addTab(cur_tab, f"{k} letter words.")

