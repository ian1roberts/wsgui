from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton
)
from PySide6.QtGui import QAction

from wssgui.imageview import ImageArea
from wssgui.wordview import WordArea
from wssgui.letter_wheel import LetterArea


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WordscapeSolver GUI")

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
        layout.addWidget(self.image_area)
        self._image_view_box.setLayout(layout)
        print("Created image panel")


    def create_letter_wheel(self):
        self._letter_view_box = QGroupBox("Letter Wheel")
        self.letter_area = LetterArea()
        layout = QVBoxLayout()
        layout.addWidget(self.letter_area)
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
        cmds = {"Load Image": self.file_load_image,
                "Analyse": self.analyse_calculate,
                "Highlight":self.analyse_display}
        for cmd in cmds:
            butt = QPushButton(cmd)
            butt.clicked.connect(cmds[cmd])
            layout.addWidget(butt)

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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Combine image and letter wheel
        left_vlay = QVBoxLayout()
        left_vlay.addWidget(self._image_view_box)
        left_vlay.addWidget(self._letter_view_box)
        # Combine Found Words and Buttons
        right_vlay = QVBoxLayout()
        right_vlay.addWidget(self._word_view_box)
        right_vlay.addWidget(self._button_box)
        # Put main view together
        layout = QHBoxLayout(central_widget)
        layout.addLayout(left_vlay)
        layout.addLayout(right_vlay)

    def gen_statusbar(self, txt = "Ready"):
        self.status = self.statusBar().showMessage(txt)

    def file_save_image(self):
        pass

    def file_load_image(self):
        pass

    def file_loaddir_image(self):
        pass

    def edit_copy(self):
        pass

    def edit_paste(self):
        pass

    def analyse_calculate(self):
        pass

    def analyse_display(self):
        pass

    def help_about(self):
        pass
