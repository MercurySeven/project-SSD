from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (QPushButton,
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

        # TODO: implement better style management
        self.setStyleSheet(
            "background-color: rgb(96,96,96); margin:5px; border:1px solid black; color: white;")
        self.runButton = QPushButton("Run", self)
        self.stopButton = QPushButton("Stop", self)

        # create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.runButton)
        self.layout.addWidget(self.stopButton)
        self.setLayout(self.layout)

        # Connecting button the signal
        self.runButton.clicked.connect(self.__run_watch)
        self.stopButton.clicked.connect(self.__stop_watch)

    @Slot()
    def __run_watch(self):
        print("called SyncWidget.__run -> emit watch(True)")  # debug
        self.Sg_watch.emit(True)

    @Slot()
    def __stop_watch(self):
        print("called watchWidget.__stop -> emit watch(False)")  # debug
        self.Sg_watch.emit(False)