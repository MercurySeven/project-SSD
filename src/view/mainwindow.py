from PySide6.QtWidgets import (QMainWindow)
from PySide6.QtGui import (QIcon)

from view.widget.mainwidget import MainWidget

from view.stylesheets.qssManager import setQss


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.setWindowIcon(QIcon("logo.png"))

        # widgets
        self.mainWidget = MainWidget(self)

        # Non più necessario ma da controllare
        # create layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.mainWidget)
        # self.setLayout(layout)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.mainWidget)

        # style
        self.resize(1200, 800)

        setQss("style.qss", self)
