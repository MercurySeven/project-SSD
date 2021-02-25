from PySide6.QtCore import (Signal, Slot, Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)


class SyncronizedWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SyncronizedWidget, self).__init__(parent)

        self.label = QLabel("<TODO Syncronized here>", self)
        self.label.setAlignment(Qt.AlignCenter)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
