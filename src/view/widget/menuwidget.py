from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget)
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtGui import QPixmap, QIcon

class MenuWidget(QWidget):

    def __init__(self, parent):

        super(MenuWidget, self).__init__(parent)

        self.setAccessibleName('MenuNav')

        fileIcon = QIcon(QPixmap(':/icons/copy.png'))
        settingsIcon = QIcon(QPixmap(':/icons/settings.png'))

        syncronizedButton = QPushButton(self)
        syncronizedButton.setIcon(fileIcon)
        syncronizedButton.setIconSize(QSize(30, 30))

        settingsButton = QPushButton(self)
        settingsButton.setIcon(settingsIcon)
        settingsButton.setIconSize(QSize(30, 30))

        # connect to actions
        syncronizedButton.clicked.connect(self.showSyncronized)
        settingsButton.clicked.connect(self.showSettings)

        # layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(syncronizedButton)
        vbox.addStretch()
        vbox.addWidget(settingsButton)
        self.setLayout(vbox)

    def showSyncronized(self):
        self.parent().swidget.setCurrentWidget(self.parent().syncronizedWidget)

    def showSettings(self):
        self.parent().swidget.setCurrentWidget(self.parent().settingsWidget)
