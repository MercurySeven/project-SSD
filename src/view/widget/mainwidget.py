from PySide6 import QtCore
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget)
from view.widget.menuwidget import MenuWidget
from view.widget.syncronizedwidget import SyncronizedWidget
from view.widget.settingswidget import SettingsWidget
from PySide6.QtCore import Qt

from view.widget.watchwidget import WatchWidget
from model.directory import Directory
import re


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

        self.menuWidget = MenuWidget(self)
        self.syncronizedWidget = SyncronizedWidget(self)

        self.settingsWidget = SettingsWidget(self)

        # self.listOfFiles = Directory(
        #     '', self.settingsWidget.settings.get_path())

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
            if re.findall("view.widget", str(i)):
                i.setAttribute(QtCore.Qt.WA_StyledBackground, True)
