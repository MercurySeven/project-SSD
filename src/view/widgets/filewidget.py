import os
from PySide6.QtWidgets import (QToolButton)
from PySide6.QtGui import (QIcon, QDesktopServices)
from PySide6.QtCore import (Qt, QSize, QTimer, Signal, QSettings, QUrl)
from src.model.file import File


class FileWidget(QToolButton):

    doubleClicked = Signal()

    def __init__(self, file: File):
        super(FileWidget, self).__init__()

        self.env_settings = QSettings()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.checkDoubleClick)

        self.doubleClicked.connect(self.onDoubleclick)

        self.setAccessibleName('File')

        file_icon = QIcon('./icons/copy.png')

        self.setIcon(file_icon)
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.name = file.get_name()
        self.creation_date = file.get_creation_date()
        self.last_modified_date = file.get_last_modified_date()
        self.type = file.get_type()
        self.size = file.get_size()
        self.status = file.get_status()

        self.setText(self.name)
        self.setToolTip("Ultima modifica: " +
                        self.last_modified_date + "\nSize: " + self.size)

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

    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()

        if self.timer.isActive() is False:
            self.timer.start(250)

    def onDoubleclick(self):
        path = os.path.join(self.env_settings.value("sync_path"), self.name)
        file_path = QUrl.fromUserInput(path)
        QDesktopServices.openUrl(file_path)
