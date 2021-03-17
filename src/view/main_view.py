from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget)
from PySide6.QtGui import (QIcon)
from PySide6 import QtCore
from PySide6.QtCore import (Slot, Signal)

import re

from src.view.stylesheets.qssManager import setQss
from src.view.widgets.watchwidget import WatchWidget
from .file_syncronized_widget import FileSyncronizedWidget
from .settings_widget import SettingsWidget
from .lateral_menu_widget import LateralMenuWidget
from src.controllers.widgets.visualize_file_controller import VisualizeFileController
from typing import TypedDict
from src.model.files_model import FilesModel


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
    # Signals
    showFiles = Signal()

    def __init__(self, parent=None):

        super(MainWidget, self).__init__(parent)
        # model
        self.files_model = FilesModel()
        # controller
        self.visualize_file_controller = VisualizeFileController(self, self.files_model)
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

        self.showFiles.connect(self.visualize_file_controller.update_visualization)

    def update_view(self, list_of_files: dict, list_of_dirs: dict) -> None:
        self.syncronizedWidget.update_content(list_of_files, list_of_dirs)
        self.swidget.setCurrentWidget(self.syncronizedWidget)

    # metodo chiamato da lateral_menu_widget per scatenare il segnale che arriva al modello per aggiornare la lista di file
    def call_controller_for_list_file(self):
        self.showFiles.emit()
