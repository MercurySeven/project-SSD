from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from PySide6.QtCore import QObject, Signal, Slot, Qt

from syncwidget import *

class MainView(QWidget):
    """This is the main view class"""

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)

        self.label = QLabel( "MainView" )
        self.label.setAlignment(Qt.AlignCenter)

        self.syncWidget = SyncWidget(self)
        # set initial status
        self.syncWidget.Sl_status(False)

        # create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.syncWidget)
        self.setLayout(self.layout)