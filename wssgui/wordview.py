from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QTabWidget,
    QVBoxLayout,
)


class WordArea(QTabWidget):
    def __init__(self) -> None:
        super().__init__()
        self.selected_word: list = list()
        self.words_set: set = set()

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
                word_button.toggled.connect(
                    lambda checked, i=i, wl=word_label: self.update_label(
                        i, wl, checked
                    )
                )
                cur_layout.addLayout(row)
                self.words_set.add(word)

            cur_tab.setLayout(cur_layout)
            self.addTab(cur_tab, f"{k} letter words.")
            self.selected_word.append(QLabel(""))

    def update_label(self, i, word_label, checked):
        if checked:
            self.selected_word[i].setText(word_label.text())

    def clear(self):
        for i in reversed(range(self.count())):
            self.removeTab(i)
            self.selected_word.pop()

    def is_member(self, word):
        if word in self.words_set:
            return True
        return False

    def found_word(self, word):
        for i in range(self.count()):
            tab = self.widget(i)
            layout = tab.layout()
            for j in range(layout.count()):
                widget = layout.itemAt(j)
                label = widget.itemAt(1).widget()
                if label.text() == word:
                    print(f"Found {word} & setting style")
                    label.setStyleSheet("color: green")
        return False
