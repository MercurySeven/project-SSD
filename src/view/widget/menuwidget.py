from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PySide6.QtCore import (Qt)

class MenuWidget(QWidget):

    def __init__(self, parent):

        super(MenuWidget, self).__init__(parent)

        self.setAccessibleName('MenuNav')

        syncronizedButton = QPushButton("🗐", self)
        diskQuotaButton = QPushButton("🖴", self)
        settingsButton = QPushButton("⚙", self)

        # connect to actions
        syncronizedButton.clicked.connect(self.showSyncronized)
        diskQuotaButton.clicked.connect(self.showDiskQuota)
        settingsButton.clicked.connect(self.showSettings)

        # layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(syncronizedButton)
        vbox.addWidget(diskQuotaButton)
        vbox.addStretch()
        vbox.addWidget(settingsButton)
        self.setLayout(vbox)

    def showSyncronized(self):
        self.parent().swidget.setCurrentWidget(self.parent().syncronizedWidget)

    def showDiskQuota(self):
        self.parent().swidget.setCurrentWidget(self.parent().diskquotaWidget)

    def showSettings(self):
        self.parent().swidget.setCurrentWidget(self.parent().settingsWidget)
