from PySide6 import QtCore
from PySide6.QtWidgets import (QGridLayout,QLabel, QLayout,QVBoxLayout, QWidget, QStackedWidget)
from view.widget.diskquotawidget import DiskQuotaWidget
from view.widget.menuwidget import MenuWidget
from view.widget.syncronizedwidget import SyncronizedWidget
from view.widget.settingswidget import SettingsWidget

from view.widget.watchwidget import WatchWidget

import re


class MainWidget(QWidget):

    def __init__(self, parent=None):

        super(MainWidget, self).__init__(parent)
        # layouts
        # Grid di struttura dell'applicazione
        self.mainGrid = QGridLayout(self)
        # finestra centrale in cui compariranno le opzioni selezionate
        self.centerWindow = QVBoxLayout(self)

        # widgets
        self.watchWidget = WatchWidget(self)

        self.menuWidget = MenuWidget(self)
        self.syncronizedWidget = SyncronizedWidget(self)

        self.diskquotaWidget = DiskQuotaWidget(self)
        self.settingsWidget = SettingsWidget(self)

        # stacked
        self.swidget = QStackedWidget()
        self.swidget.addWidget(self.syncronizedWidget)
        self.swidget.addWidget(self.diskquotaWidget)
        self.swidget.addWidget(self.settingsWidget)

        # create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.watchWidget)
        layout.addWidget(self.menuWidget)
        self.centerWindow.addWidget(self.swidget)
        self.mainGrid.addLayout(layout, 0, 0, 1, 2)
        self.mainGrid.addLayout(self.centerWindow, 0, 2, 0, 4)
        self.setLayout(self.mainGrid)

        # stylesheet
        for i in self.findChildren(QWidget, ):
            if(re.findall("view.widget", str(i))):
                i.setAttribute(QtCore.Qt.WA_StyledBackground, True)
