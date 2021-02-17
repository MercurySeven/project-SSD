from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget, QStackedWidget)
from PySide6.QtCore import Signal, Slot, Qt

from view.widget.syncwidget import SyncWidget
from view.widget.menuwidget import MenuWidget
from view.widget.syncronizedwidget import SyncronizedWidget
from view.widget.diskquotawidget import DiskQuotaWidget
from view.widget.settingswidget import SettingsWidget


class MainWidget(QWidget):
    
    def __init__(self, parent=None):
        
        super(MainWidget, self).__init__(parent)

        # widgets
        self.syncWidget = SyncWidget(self)
        self.syncWidget.Sl_status(False)  # set initial status

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
        layout = QVBoxLayout()
        layout.addWidget(self.syncWidget)
        layout.addWidget(self.menuWidget)
        layout.addWidget(self.swidget)
        self.setLayout(layout)