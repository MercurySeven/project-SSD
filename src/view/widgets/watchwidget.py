from PySide6.QtCore import Signal, Slot, Qt, QSize
from PySide6.QtWidgets import (QPushButton, QLabel,
                               QVBoxLayout, QWidget)
from PySide6.QtGui import QPixmap, QIcon


class WatchWidget(QWidget):
    """the WatchWidget class allows the GUI to activate or deactivate the watchdog

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
        self.watch_label.setText("SYNC")
        self.watch_label.setAccessibleName('Title')

        self.running_label = QLabel(self)
        self.running_label.setAlignment(Qt.AlignCenter)
        self.running_label.setText("disattivata")
        self.running_label.setAccessibleName('Subtitle')

        self.syncButton = QPushButton(self)
        syncIcon = QIcon(QPixmap(':/icons/reload.png'))
        self.syncButton.setIcon(syncIcon)
        self.syncButton.setIconSize(QSize(50, 50))
        self.syncButton.setCheckable(True)
        self.syncButton.setChecked(False)
        self.syncButton.setAccessibleName('HighlightButton')
        # self.syncButton.setCheckable(True)

        self.menu_label = QLabel(self)
        self.menu_label.setAlignment(Qt.AlignCenter)
        self.menu_label.setText("• • •")

        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.watch_label)
        self.layout.addWidget(self.running_label)
        self.layout.addWidget(self.syncButton)
        self.layout.addWidget(self.menu_label)
        self.setLayout(self.layout)

        # Connecting button the signal
        self.syncButton.clicked.connect(self.startStop)

    @Slot()
    def __run_watch(self):
        print("called WatchWidget.__run -> emit watch(True)")  # debug
        self.running_label.setText("attivata")
        self.Sg_watch.emit(True)

    @Slot()
    def __stop_watch(self):
        print("called WatchWidget.__stop -> emit watch(False)")  # debug
        self.running_label.setText("disattivata")
        self.Sg_watch.emit(False)

    def startStop(self):
        print(self.syncButton.isChecked())
        if(self.syncButton.isChecked()):
            self.__run_watch()
        else:
            self.__stop_watch()
