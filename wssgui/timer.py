from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class TimerWidget(QWidget):
    timer_timeout = Signal(bool)
    
    def __init__(self, target, interval, parent=None):
        super(TimerWidget, self).__init__(parent)
        self.timer = QTimer()
        self.target = QLabel(f"Target:\n\t{target} minutes\n")
        self.label = QLabel("Elapsed time:\n\t0 minute(s)")
        self.elapsed_minutes = 0
        self.target_minutes = int(target)
        self.interval = int(interval)

        layout = QVBoxLayout(self)
        layout.addWidget(self.target)
        layout.addWidget(self.label)
        self.timer.timeout.connect(self.show_time)

    def start_timer(self):
        self.timer.start(self.interval)

    def show_time(self):
        self.elapsed_minutes += 1
        self.label.setText(f"Elapsed time:\n\t{self.elapsed_minutes} minute(s)")
        if self.elapsed_minutes == self.target_minutes:
            self.timer.stop()
            self.label.setText("Elapsed time: Target reached!")
            self.timer_timeout.emit(True)

if __name__ == "__main__":
    app = QApplication([])
    widget = TimerWidget(10, 1000)
    widget.start_timer()
    widget.show()
    app.exec()
