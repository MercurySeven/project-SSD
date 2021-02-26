from PySide6.QtWidgets import (QVBoxLayout, QWidget, QStackedWidget)
from src.view.widget.diskquotawidget import DiskQuotaWidget
from src.view.widget.syncwidget import SyncWidget
from src.view.widget.menuwidget import MenuWidget
from src.view.widget.syncronizedwidget import SyncronizedWidget
from src.view.widget.settingswidget import SettingsWidget

from src.view.widget.watchwidget import WatchWidget


class MainWidget(QWidget):

    def __init__(self, parent=None):

        super(MainWidget, self).__init__(parent)
        # widgets
        self.syncWidget = SyncWidget(self)
        self.syncWidget.Sl_status(False)  # set initial status

        self.watchWidget = WatchWidget(self)

        self.menuWidget = MenuWidget(self)
        self.syncronizedWidget = SyncronizedWidget(self)

        self.diskquotaWidget = DiskQuotaWidget(self)
        self.settingsWidget = SettingsWidget(self)

        # stacked
        self.swidget = QStackedWidget()
        self.swidget.addWidget(self.watchWidget)
        self.swidget.addWidget(self.syncronizedWidget)
        self.swidget.addWidget(self.diskquotaWidget)
        self.swidget.addWidget(self.settingsWidget)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.syncWidget)
        layout.addWidget(self.menuWidget)
        layout.addWidget(self.swidget)
        self.setLayout(layout)
