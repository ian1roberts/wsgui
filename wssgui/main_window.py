from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QFileDialog
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from wssgui.imageview import ImageArea
from wssgui.wordview import WordArea
from wssgui.letter_wheel import LetterArea
from click.testing import CliRunner
from wordscapesolver.cli.solveit import solveit

class ResultsParse(object):
    def __init__(self, output):
        self.output = output
        self.words = dict()
        self.letters = ""
        self.parse_it()

    def parse_it(self):
        num = 0
        for line in self.output:

            if ((not line) or
                (":" in line) or
                (".png" in line) or
                ("=" in line)):
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

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WordscapeSolver GUI")
        self.setGeometry(30, 30, 600, 800)

        # Create menus and Status
        self.gen_menubar()
        self.gen_statusbar()

        # Display the main view area
        self.create_image_view_panel()
        self.create_letter_wheel()
        self.create_word_view_panel()
        self.create_buttons()
        self.gen_mainview()

    def create_image_view_panel(self):
        self._image_view_box = QGroupBox("Puzzle Image")
        layout = QVBoxLayout()
        self.image_area = ImageArea()
        layout.addWidget(self.image_area.container)
        self._image_view_box.setLayout(layout)
        print("Created image panel")


    def create_letter_wheel(self):
        self._letter_view_box = QGroupBox("Letter Wheel")
        self.letter_area = LetterArea()
        layout = QVBoxLayout()
        layout.addWidget(self.letter_area.view)
        self._letter_view_box.setLayout(layout)
        print("Created letter view panel")

    def create_word_view_panel(self):
        self._word_view_box = QGroupBox("Found Words")
        layout = QVBoxLayout()
        self.word_area = WordArea()
        layout.addWidget(self.word_area)
        self._word_view_box.setLayout(layout)
        print("Created image panel")

    def create_buttons(self):
        self._button_box = QGroupBox("Controls")
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        cmds = {"Load Image": self.file_load_image,
                "Analyse": self.analyse_calculate,
                "Highlight":self.analyse_display,
                "Clear": self.analyse_clear,
                "Quit": QApplication.quit}
        
        col = -1
        for i, cmd in enumerate(cmds):
            col += 1
            row = 0
            butt = QPushButton(cmd)
            butt.clicked.connect(cmds[cmd])
            if i % 2 == 1:
                row = 1
                col -= 1
            layout.addWidget(butt, row, col)

        self._button_box.setLayout(layout)
        print("Created button panel")


    def gen_menubar(self):
        file_menu = self.menuBar().addMenu('&File')
        edit_menu = self.menuBar().addMenu('&Edit')
        analyse_menu = self.menuBar().addMenu('&Analyse')
        help_menu = self.menuBar().addMenu('&Help')

        # Add actions to the File menu
        load_action = QAction("&Load", self)
        loaddir_action = QAction("Load &Directory", self)
        save_action = QAction('&Save', self)
        quit_action = QAction("&Quit", self)
        save_action.triggered.connect(self.file_save_image)
        load_action.triggered.connect(self.file_load_image)
        loaddir_action.triggered.connect(self.file_loaddir_image)
        quit_action.triggered.connect(QApplication.quit)
        file_menu.addActions([load_action, loaddir_action,
                              save_action, quit_action])

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
        left_vlay.addWidget(self._image_view_box, stretch = 2)
        left_vlay.addWidget(self._letter_view_box, stretch = 1)
        # Combine Found Words and Buttons
        right_vlay = QVBoxLayout()
        right_vlay.addWidget(self._word_view_box, stretch = 2)
        right_vlay.addWidget(self._button_box, stretch = 1)
        # Put main view together
        layout = QHBoxLayout(central_widget)
        layout.addLayout(left_vlay, stretch = 1)
        layout.addLayout(right_vlay, stretch = 2)

    def gen_statusbar(self, txt = "Ready"):
        self.status = self.statusBar().showMessage(txt)

    def file_save_image(self):
        pass

    def file_load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "PNG Files (*.png)")
        if file_name:
            self.image_area.load_image(file_name)
            self.image_area.container.show()
            self.image_file_name = file_name
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
        result = runner.invoke(solveit, [self.image_file_name, "-"],
                               catch_exceptions = False)
        observed = ResultsParse(result.output.split("\n"))
        self.letter_area.make_word(observed.letters)
        self.word_area.create_tabs(observed.words)


    def analyse_display(self):
        idx = self.word_area.currentIndex()
        cur_word = self.word_area.selected_word[idx].text()
        self.gen_statusbar(cur_word)
        self.letter_area.word_path(cur_word)

    def analyse_clear(self):
        last_path = self.letter_area.last_path
        if last_path:
            self.letter_area.scene.removeItem(last_path)

    def help_about(self):
        pass
