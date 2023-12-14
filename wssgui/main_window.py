from click.testing import CliRunner
from PySide6.QtCore import Property, Qt, Signal  # type: ignore
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox
)
from wordscapesolver.cli.solveit import solveit  # type: ignore

from wssgui.imageview import ImageArea
from wssgui.letter_wheel import LetterArea
from wssgui.make_words import MakeWordArea
from wssgui.wordview import WordArea
from wssgui.timer import TimerWidget


class ResultsParse(object):
    def __init__(self, output):
        self.output = output
        self.words = dict()
        self.letters = ""
        self.parse_it()

    def parse_it(self):
        num = 0
        for line in self.output:
            if (not line) or (":" in line) or (".png" in line) or ("=" in line):
                continue

            if line[0].isnumeric():
                num = int(line[0])
                self.words[num] = list()
                continue

            if not line.startswith("\t"):
                self.letters = line.strip()
            else:
                self.words[num].append(line.strip())


class MainWindow(QMainWindow):
    valueChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.buttons = dict()
        self.setWindowTitle("WordscapeSolver GUI")
        self.setGeometry(30, 30, 600, 800)

        # Create menus and Status
        self.gen_menubar()
        self.gen_statusbar()

        # Display the main view area
        self.create_image_view_panel()
        self.create_letter_wheel()
        self.create_word_view_panel()
        self.create_make_word_panel()
        self.create_buttons()
        self.create_score_panel()
        self.create_timer_view_panel(10, 60000)
        self.gen_mainview()

        # Detects a letter being selected
        # Action is only one a changed letter
        self._value = ""
        self.letter_area.view.mouseOverWidget.connect(
            lambda x: self.change_value(x.alpha)
        )

        # Adds the selected letter to the make word area
        # Chains to the previous signal
        self.valueChanged.connect(lambda alpha: self.make_word_area.add_letter(alpha))

        # Clears any highlighted blue letters
        self.letter_area.view.clearHighlight.connect(self.letter_area.deselect)

        # Releasing moues button clears the green path
        self.letter_area.view.mouseReleaseProc.connect(
            lambda word: self.analyse_valid_words(word)
        )

        # Timer has reached the target
        self.timer_area.timer_timeout.connect(
            self.game_over)

    @Property(str, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter #type: ignore
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(new_value)

    def change_value(self, alpha):
        self.value = alpha

    def create_image_view_panel(self):
        self._image_view_box = QGroupBox("Puzzle Image")
        layout = QVBoxLayout()
        self.image_area = ImageArea()
        layout.addWidget(self.image_area.container)
        self._image_view_box.setLayout(layout)

    def create_letter_wheel(self):
        self._letter_view_box = QGroupBox("Letter Wheel")
        self.letter_area = LetterArea()
        layout = QVBoxLayout()
        layout.addWidget(self.letter_area.view)
        self._letter_view_box.setLayout(layout)

    def create_make_word_panel(self):
        self._make_word_view_box = QGroupBox("Make Words")
        self.make_word_area = MakeWordArea()
        layout = QVBoxLayout()
        layout.addWidget(self.make_word_area.view)
        self._make_word_view_box.setLayout(layout)

    def create_word_view_panel(self):
        self._word_view_box = QGroupBox("Found Words")
        layout = QVBoxLayout()
        self.word_area = WordArea()
        layout.addWidget(self.word_area)
        self._word_view_box.setLayout(layout)

    def create_timer_view_panel(self, target, interval):
        self._timer_view_box = QGroupBox("Timer")
        layout = QVBoxLayout()
        self.timer_area = TimerWidget(target, interval)
        layout.addWidget(self.timer_area)
        self._timer_view_box.setLayout(layout)

    def create_buttons(self):
        self._button_box = QGroupBox("Controls")
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        cmds = {
            "Load Image": self.file_load_image,
            "Analyse": self.analyse_calculate,
            "Highlight": self.analyse_display,
            "Clear Word": self.make_word_area.clear,
            "Deselct": self.letter_area.deselect,
            "Quit": QApplication.quit,
        }

        col = -1
        for i, cmd in enumerate(cmds):
            col += 1
            row = 0
            butt = QPushButton(cmd)
            if i > 0 and i < len(cmds) - 1:
                butt.setEnabled(False)
            butt.clicked.connect(cmds[cmd])
            if i % 2 == 1:
                row = 1
                col -= 1
            layout.addWidget(butt, row, col)
            self.buttons[cmd] = butt

        self._button_box.setLayout(layout)

    def create_score_panel(self):
        self._score_view_box = QGroupBox("Score")
        layout = QVBoxLayout()
        layout.addWidget(self.word_area.score_panel)
        self._score_view_box.setLayout(layout)

    def gen_menubar(self):
        file_menu = self.menuBar().addMenu("&File")
        edit_menu = self.menuBar().addMenu("&Edit")
        analyse_menu = self.menuBar().addMenu("&Analyse")
        help_menu = self.menuBar().addMenu("&Help")

        # Add actions to the File menu
        load_action = QAction("&Load", self)
        loaddir_action = QAction("Load &Directory", self)
        save_action = QAction("&Save", self)
        quit_action = QAction("&Quit", self)
        save_action.triggered.connect(self.file_save_image)
        load_action.triggered.connect(self.file_load_image)
        loaddir_action.triggered.connect(self.file_loaddir_image)
        quit_action.triggered.connect(QApplication.quit)
        file_menu.addActions([load_action, loaddir_action, save_action, quit_action])

        # Add actions to the Edit menu
        copy_action = QAction("&Copy", self)
        paste_action = QAction("&Paste", self)
        copy_action.triggered.connect(self.edit_copy)
        paste_action.triggered.connect(self.edit_paste)
        edit_menu.addActions([copy_action, paste_action])

        # Add actions to the Analyse menu
        calculate_action = QAction("&Calculate words", self)
        display_action = QAction("&Display word", self)
        calculate_action.triggered.connect(self.analyse_calculate)
        display_action.triggered.connect(self.analyse_display)
        analyse_menu.addActions([calculate_action, display_action])

        # Add actions to the Help menu
        about_action = QAction("&About wwsg", self)
        about_action.triggered.connect(self.help_about)
        help_menu.addAction(about_action)

    def gen_mainview(self):
        # Layout = 2 columns, 2 rows
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Combine image and letter wheel
        left_vlay = QVBoxLayout()
        left_vlay.addWidget(self._image_view_box, stretch=2)
        left_vlay.addWidget(self._letter_view_box, stretch=1)
        # Combine Found Words and Buttons
        right_vlay = QVBoxLayout()
        right_hlay = QHBoxLayout()
        right_vlay.addWidget(self._word_view_box, stretch=1)
        right_vlay.addWidget(self._make_word_view_box, stretch=1)
        right_hlay.addWidget(self._timer_view_box, stretch=1)
        right_hlay.addWidget(self._score_view_box, stretch=1)
        right_vlay.addLayout(right_hlay)
        right_vlay.addWidget(self._button_box, stretch=1)
        # Put main view together
        layout = QHBoxLayout(central_widget)
        layout.addLayout(left_vlay, stretch=1)
        layout.addLayout(right_vlay, stretch=2)

    def gen_statusbar(self, txt="Ready"):
        self.status = self.statusBar().showMessage(txt)

    def game_over(self):
        msg_box = QMessageBox()
        msg_box.setText("Time's up!")
        msg_box.setInformativeText("Do you want to play again?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec()

        if result == QMessageBox.Yes:
            self.file_load_image()


    def file_save_image(self):
        pass

    def file_load_image(self):
        if self.image_area.loaded:
            for i, (_, butt) in enumerate(self.buttons.items()):
                if i > 0 and i < 4:
                    butt.setEnabled(False)
            self.image_area.reset()
            self.letter_area.deselect()
            self.word_area.clear()

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "PNG Files (*.png)"
        )
        if file_name:
            self.image_area.load_image(file_name)
            self.image_area.container.show()
            self.image_file_name = file_name
            self.buttons["Analyse"].setEnabled(True)
            self.analyse_calculate()
            self.timer_area.start_timer()
        else:
            self.close()

    def file_loaddir_image(self):
        pass

    def edit_copy(self):
        pass

    def edit_paste(self):
        pass

    def analyse_calculate(self):
        runner = CliRunner()
        result = runner.invoke(
            solveit, [self.image_file_name, "-"], catch_exceptions=False
        )
        observed = ResultsParse(result.output.split("\n"))
        self.letter_area.make_word(observed.letters)
        self.word_area.create_tabs(observed.words)
        self.word_area.create_score_panel()
        for butt in self.buttons:
            if not self.buttons[butt].isEnabled():
                self.buttons[butt].setEnabled(True)

        self.word_data = observed

    def analyse_display(self):
        idx = self.word_area.currentIndex()
        if idx < 0:
            return
        cur_word = self.word_area.selected_word[idx].text()
        if cur_word:
            self.gen_statusbar(cur_word)
            self.letter_area.word_path(cur_word)

    def analyse_valid_words(self, word):
        if self.word_area.is_member(word):
            hit = self.word_area.found_word(word)
            if hit:
                nletters = len(word)
                hits = self.word_area.update_score(nletters - 3)
                self.update_score(nletters, hits)
        self.make_word_area.clear()

    def update_score(self, letter_words, found_words):
        panel = self.word_area.score_panel.layout()
        for i in range(panel.count()):
            row = panel.itemAt(i)
            if row.itemAt(0).widget().text().startswith(f"{letter_words}"):
                row.itemAt(1).widget().setText(f"{found_words:>2}")
                max_words = int(row.itemAt(2).widget().text().split(" ")[-2])
                if int(found_words) == max_words:
                    for i in range(row.count()):
                        widget = row.itemAt(i).widget()
                        if widget is not None:
                            widget.setStyleSheet("color: green;")

    def help_about(self):
        pass
