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
        self.elapsed_seconds = 0
        self.target_minutes = int(target)
        self.interval = int(interval)

        layout = QVBoxLayout(self)
        layout.addWidget(self.target)
        layout.addWidget(self.label)
        self.timer.timeout.connect(self.update_remaining_time)

    def start_timer(self):
        self.timer.start(self.interval)

    def update_remaining_time(self):
        self.elapsed_seconds += 1
        if self.elapsed_seconds % 6 == 0:
            self.elapsed_minutes += 1

        remaining_time = self.target_minutes * 6 - self.elapsed_seconds

        if remaining_time > 6:
            self.label.setText(f"Time Remaining:\n\t{remaining_time // 6} minute(s)")
        else:
            self.label.setText(f"Time Remaining:\n\t{remaining_time * 10} seconds")

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
