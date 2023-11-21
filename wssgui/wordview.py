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
        self.selected_word = list()

    def create_tabs(self, all_words):
        for i, (k, words) in enumerate(all_words.items()):
            cur_tab = QFrame()
            cur_layout = QVBoxLayout()
            cur_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            for word in words:
                row = QHBoxLayout()
                word_button = QRadioButton()
                word_label = QLabel(word)
                row.addWidget(word_button)
                row.addWidget(word_label)
                word_button.toggled.connect(lambda checked,
                    i=i, wl=word_label:
                        self.update_label(i, wl, checked))
                cur_layout.addLayout(row)

            cur_tab.setLayout(cur_layout)
            self.addTab(cur_tab, f"{k} letter words.")
            self.selected_word.append(QLabel(""))

    def update_label(self, i, word_label, checked):
        if checked:
            self.selected_word[i].setText(word_label.text())