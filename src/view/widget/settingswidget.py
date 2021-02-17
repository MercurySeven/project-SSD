from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)


class SettingsWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        self.label = QLabel("<TODO Settings here>", self)
        self.label.setAlignment(Qt.AlignCenter)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)