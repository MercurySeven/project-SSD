from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget)
from PySide6.QtGui import (QIcon)
from PySide6 import QtCore

import re

from src.view.stylesheets.qssManager import setQss
from src.view.widgets import (WatchWidget)
from .file_syncronized_widget import FileSyncronizedWidget
from .settings_widget import SettingsWidget
from .lateral_menu_widget import LateralMenuWidget


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


class MainWidget(QWidget):

    def __init__(self, parent=None):

        super(MainWidget, self).__init__(parent)
        # layouts
        # Grid di struttura dell'applicazione
        self.mainGrid = QHBoxLayout(self)
        self.mainGrid.setContentsMargins(0, 0, 0, 0)
        # finestra centrale in cui compariranno le opzioni selezionate
        self.central_view = QVBoxLayout()
        self.central_view.setSpacing(0)

        # widgets
        self.watchWidget = WatchWidget(self)

        self.menuWidget = LateralMenuWidget(self)

        self.syncronizedWidget = FileSyncronizedWidget(self)

        self.settingsWidget = SettingsWidget(self)

        # stacked
        self.swidget = QStackedWidget()
        self.swidget.setAccessibleName("Stacked")
        self.swidget.addWidget(self.syncronizedWidget)
        self.swidget.addWidget(self.settingsWidget)

        # create layout
        self.menu_laterale = QVBoxLayout()
        self.menu_laterale.addWidget(self.watchWidget)
        self.menu_laterale.addWidget(self.menuWidget)
        self.menu_laterale.setSpacing(0)

        self.central_view.addWidget(self.swidget)
        self.mainGrid.addLayout(self.menu_laterale)
        self.mainGrid.addLayout(self.central_view)
        # self.setLayout(self.mainGrid)

        # stylesheet
        for i in self.findChildren(QWidget, ):
            if re.findall("view", str(i)):
                i.setAttribute(QtCore.Qt.WA_StyledBackground, True)
                print(i)
