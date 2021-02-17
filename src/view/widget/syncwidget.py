from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (QLabel, QPushButton,
                               QVBoxLayout, QWidget)


class SyncWidget(QWidget):
    """the SyncWidget class allows to activate or deactivate
    and see the synchronization status through the emission
    of the 'sync' signal

    Signals
    -------
    sync: bool
        emit True for activate synconization
        emit false for deactivate syncronization

    Slots
    -----
    __run()
        private slot
        when run button is clicked emit sync(True)

    __stop()
        private slot
        when stop button is clicked emit sync(False)

    Sl_status(stat: bool)
        public slot
        receive a 'status' signal and change label to show
        the synchronization status

    """

    # creating Signals
    Sg_sync = Signal(bool)

    def __init__(self, parent=None):
        super(SyncWidget, self).__init__(parent)

        # TODO: implement better style management
        self.setStyleSheet(
            "background-color: rgb(96,96,96); margin:5px; border:1px solid black; color: white;")

        # provvisoria
        self.text = lambda x: "Synchronization is running" if x else "Synchronization is stopped"

        self.label = QLabel(self.text(False), self)
        self.label.setAlignment(Qt.AlignCenter)

        self.runButton = QPushButton("Run", self)
        self.stopButton = QPushButton("Stop", self)

        # create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.runButton)
        self.layout.addWidget(self.stopButton)
        self.setLayout(self.layout)

        # Connecting button the signal
        self.runButton.clicked.connect(self.__run)
        self.stopButton.clicked.connect(self.__stop)

    @Slot()
    def __run(self):
        print("called SyncWidget.__run -> emit sync(True)")  # debug
        self.Sg_sync.emit(True)

    @Slot()
    def __stop(self):
        print("called SyncWidget.__stop -> emit sync(False)")  # debug
        self.Sg_sync.emit(False)

    @Slot(bool)
    def Sl_status(self, stat: bool):
        print("called SyncWidget.Sl_status -> change label")
        self.label.setText(self.text(stat))
