from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget)


class MenuWidget(QWidget):

    def __init__(self, parent):

        super(MenuWidget, self).__init__(parent)

        syncronizedButton = QPushButton('SINCRONIZZATI', self)
        diskQuotaButton = QPushButton('QUOTA DISCO', self)
        settingsButton = QPushButton('SETTINGS', self)

        # connect to actions
        syncronizedButton.clicked.connect(self.showSyncronized)
        diskQuotaButton.clicked.connect(self.showDiskQuota)
        settingsButton.clicked.connect(self.showSettings)

        # layout
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(syncronizedButton)
        vbox.addWidget(diskQuotaButton)
        vbox.addWidget(settingsButton)
        vbox.addStretch()
        self.setLayout(vbox)

    def showSyncronized(self):
        self.parent().swidget.setCurrentWidget(self.parent().syncronizedWidget)

    def showDiskQuota(self):
        self.parent().swidget.setCurrentWidget(self.parent().diskquotaWidget)

    def showSettings(self):
        self.parent().swidget.setCurrentWidget(self.parent().settingsWidget)
