from PySide6.QtWidgets import (QHBoxLayout, QWidget, QToolButton, QLabel, QVBoxLayout)
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QTimer, Signal, Slot, QSettings

from subprocess import call
import os


class FileWidget(QToolButton):

    doubleClicked = Signal()
    clicked = Signal()

    def __init__(self, name, creation_date, last_modified_date, type, size, status):
        super(FileWidget, self).__init__()

        self.env_settings = QSettings()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

        self.doubleClicked.connect(self.onDoubleclick)

        self.setAccessibleName('File')

        fileIcon = QIcon(QPixmap(':/icons/copy.png'))

        self.setIcon(fileIcon)
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.name = str(name)
        self.creation_date = str(creation_date)
        self.last_modified_date = str(last_modified_date)
        self.type = str(type)
        self.size = str(size), self
        self.status = str(status)

        self.setText(self.name)

        '''self.contextWindow = QWidget()
        self.contextWindow.nameLabel = QLabel()
        self.contextWindow.nameLabel.setText(self.name)
        self.contextWindow.typeLabel = QLabel()
        self.contextWindow.typeLabel.setText(self.type)
        contextLayout = QVBoxLayout()
        contextLayout.addWidget(self.contextWindow.nameLabel)
        contextLayout.addWidget(self.contextWindow.typeLabel)
        self.contextWindow.setLayout(contextLayout)

        self.setLayout(QVBoxLayout())
        
        self.layout().addWidget(self.contextWindow)'''
        # add fields to structure

    @Slot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)

    def onDoubleclick(self):
        call(['xdg-open', self.env_settings.value("sync_path") + '/' + self.name])

