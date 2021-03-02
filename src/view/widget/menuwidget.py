from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtGui import QPixmap, QIcon

class MenuWidget(QWidget):

    def __init__(self, parent):

        super(MenuWidget, self).__init__(parent)

        self.setAccessibleName('MenuNav')

        fileIcon = QIcon(QPixmap(':/icons/copy.png'))
        settingsIcon = QIcon(QPixmap(':/icons/settings.png'))

        self.syncronizedButton = QPushButton(self)
        self.syncronizedButton.setIcon(fileIcon)
        self.syncronizedButton.setIconSize(QSize(30, 30))
        self.syncronizedButton.setCheckable(True)

        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(settingsIcon)
        self.settingsButton.setIconSize(QSize(30, 30))
        self.settingsButton.setCheckable(True)
        self.syncronizedButton.setChecked(False)

        # connect to actions
        self.syncronizedButton.clicked.connect(self.showSyncronized)
        self.settingsButton.clicked.connect(self.showSettings)

        # layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.syncronizedButton)
        vbox.addStretch()
        vbox.addWidget(self.settingsButton)
        self.setLayout(vbox)

        self.syncronizedButton.setChecked(True)

    def showSyncronized(self):
        self.parent().swidget.setCurrentWidget(self.parent().syncronizedWidget)
        self.settingsButton.setChecked(False)
        self.syncronizedButton.setChecked(True)

    def showSettings(self):
        self.parent().swidget.setCurrentWidget(self.parent().settingsWidget)
        self.syncronizedButton.setChecked(False)
        self.settingsButton.setChecked(True)
