from PySide6.QtCore import Qt, QTimer
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
        self.scoring: dict = dict()
        self.score_panel = QFrame()
        self.timer = QTimer()

    @property
    def nwords(self):
        return len(self.words_set)

    @property
    def nfound(self):
        return sum(
            [self.update_score(k - 3) for k in self.scoring.keys()]
        )

    @property
    def percent_score(self):
        return f"{self.nfound / self.nwords * 100:.1f}%"

    def create_tabs(self, all_words):
        for i, (k, words) in enumerate(all_words.items()):
            cur_tab = QFrame()
            cur_layout = QVBoxLayout()
            cur_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            found = 0
            for word in words:
                row = QHBoxLayout()
                word_button = QRadioButton()
                word_button.setEnabled(False)
                word_label = QLabel(word)
                word_label.setStyleSheet("color: white")
                row.addWidget(word_button)
                row.addWidget(word_label)
                word_button.toggled.connect(
                    lambda checked, i=i, wl=word_label: self.update_label(
                        i, wl, checked
                    )
                )
                cur_layout.addLayout(row)
                self.words_set.add(word)
                if word_button.isEnabled():
                    found += 1

            cur_tab.setLayout(cur_layout)
            self.addTab(cur_tab, f"{k} letter words.")
            self.selected_word.append(QLabel(""))
            self.scoring[k] = (cur_layout.count(), found)

    def create_score_panel(self):
        x = 0
        score_layout = QVBoxLayout()
        score_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        for k, (v, _) in self.scoring.items():
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            row.addWidget(QLabel(f"{k} letter words: "))
            row.addWidget(QLabel(f"{x:>2}"))
            row.addWidget(QLabel(f"/ {v:>2} found."))
            score_layout.addLayout(row)
        qscore = QLabel("Score: ")
        qscore.setObjectName("score")
        score_layout.addWidget(qscore)
        self.score_panel.setLayout(score_layout)

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
                button = widget.itemAt(0).widget()
                if label.text() == word:
                    label.setStyleSheet("color: green")
                    button.setEnabled(True)
                    return True
        return False

    def update_score(self, i):
        hit = 0
        tab = self.widget(i)
        layout = tab.layout()
        for j in range(layout.count()):
            widget = layout.itemAt(j)
            button = widget.itemAt(0).widget()
            if button.isEnabled():
                hit += 1
        return hit
