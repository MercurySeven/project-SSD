from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QMainWindow)

from view.widget.mainwidget import MainWidget


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.label = QLabel("MainWindow", self)
        self.label.setAlignment(Qt.AlignCenter)

        # widgets
        self.mainWidget = MainWidget(self)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.mainWidget)
        self.setLayout(layout)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.mainWidget)

        # style
        self.resize(800, 600)
