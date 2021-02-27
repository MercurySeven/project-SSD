from PySide6.QtWidgets import (QVBoxLayout, QMainWindow)

from view.widget.mainwidget import MainWidget


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")

        # widgets
        self.mainWidget = MainWidget(self)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.mainWidget)
        self.setLayout(layout)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.mainWidget)

        # style
        self.resize(1200, 800)
