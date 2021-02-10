from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)
from PySide6.QtCore import Qt

from view.widget.syncwidget import SyncWidget


class MainView(QWidget):
    """This is the main view class"""

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.label = QLabel("MainView")
        self.label.setAlignment(Qt.AlignCenter)

        self.syncWidget = SyncWidget(self)
        # set initial status
        self.syncWidget.Sl_status(False)

        # create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.syncWidget)
        self.setLayout(self.layout)
