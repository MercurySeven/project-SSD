from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (QPushButton, QLabel,
                               QVBoxLayout, QWidget)


class WatchWidget(QWidget):
    """the WatchWidget class allows to activate or deactivate the watchdog

    Signals
    -------
    watch: bool
        emit True for activate watchdog
        emit false for deactivate watchdog

    Slots
    -----
    __run()
        private slot
        when run button is clicked emit watch(True)

    __stop()
        private slot
        when stop button is clicked emit watch(False)
    """

    # creating Signals
    Sg_watch = Signal(bool)

    def __init__(self, parent=None):
        super(WatchWidget, self).__init__(parent)

        self.watch_label = QLabel(self)
        self.watch_label.setAlignment(Qt.AlignCenter)
        self.watch_label.setText("STATO SYNC")

        self.running_label = QLabel(self)
        self.running_label.setAlignment(Qt.AlignCenter)
        self.running_label.setText("disattivata")

        self.runButton = QPushButton("Run", self)
        self.stopButton = QPushButton("Stop", self)

        self.menu_label = QLabel(self)
        self.menu_label.setAlignment(Qt.AlignCenter)
        self.menu_label.setText("_____________")

        # create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.watch_label)
        self.layout.addWidget(self.running_label)
        self.layout.addWidget(self.runButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.menu_label)
        self.setLayout(self.layout)

        # Connecting button the signal
        self.runButton.clicked.connect(self.__run_watch)
        self.stopButton.clicked.connect(self.__stop_watch)

    @Slot()
    def __run_watch(self):
        print("called SyncWidget.__run -> emit watch(True)")  # debug
        self.running_label.setText("attivata")
        self.Sg_watch.emit(True)

    @Slot()
    def __stop_watch(self):
        print("called watchWidget.__stop -> emit watch(False)")  # debug
        self.running_label.setText("disattivata")
        self.Sg_watch.emit(False)
