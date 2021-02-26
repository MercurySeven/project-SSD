from PySide6.QtWidgets import (QVBoxLayout, QWidget, QStackedWidget)
from view.widget.diskquotawidget import DiskQuotaWidget
from view.widget.menuwidget import MenuWidget
from view.widget.syncronizedwidget import SyncronizedWidget
from view.widget.settingswidget import SettingsWidget

from view.widget.watchwidget import WatchWidget


class MainWidget(QWidget):

    def __init__(self, parent=None):

        super(MainWidget, self).__init__(parent)

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
        layout = QVBoxLayout()
        layout.addWidget(self.watchWidget)
        layout.addWidget(self.menuWidget)
        layout.addWidget(self.swidget)
        self.setLayout(layout)
