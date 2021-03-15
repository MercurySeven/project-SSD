from PySide6.QtWidgets import (QMainWindow)
from PySide6.QtGui import (QIcon)

from src.view.stylesheets.qssManager import setQss
from .main_widget import MainWidget


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.setWindowIcon(QIcon("./icons/logo.png"))

        # widgets
        self.mainWidget = MainWidget(self)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.mainWidget)

        # style
        self.resize(1200, 800)

        setQss("style.qss", self)
