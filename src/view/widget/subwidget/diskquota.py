from PySide6.QtWidgets import (
    QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)
from PySide6.QtCore import (QSettings, Signal)
from PySide6.QtGui import (QIntValidator)

import os
import math

import settings

from PySide6.QtCore import Qt



class diskQuota(QWidget):

    Sg_update_space = Signal()

    def __init__(self, parent=None):
        super(diskQuota, self).__init__(parent)

        self.env_settings = QSettings()

        self.setAccessibleName('InfoBox')

        self.folderSize = 0
        maxSize = settings.get_quota_disco()

        # Barra riempimento disco

        self.progressLabel = QLabel(self)
        self.progressLabel.setText('Spazio occupato')
        self.progressLabel.setAccessibleName('Subtitle')

        self.diskProgress = QProgressBar()
        self.diskProgress.setFormat('')
        self.diskProgress.setRange(0, maxSize)
        self.diskProgress.setValue(self.folderSize)
        self.diskQuota = QLabel()
        self.diskQuota.setText(
            f"{self.folderSize} su {self.convert_size(maxSize)}")

        # Modifica spazio dedicato

        self.spaceLabel = QLabel('Spazio dedicato')
        self.spaceLabel.setAccessibleName('Subtitle')

        self.dedicatedSpace = QLineEdit()
        onlyInt = QIntValidator()
        self.dedicatedSpace.setValidator(onlyInt)
        self.dedicatedSpace.setText(str(maxSize))

        self.dedicatedSpace.returnPressed.connect(self.aggiorna)

        diskLayout = QVBoxLayout()
        diskLayout.setAlignment(Qt.AlignLeft)
        diskLayout.addWidget(self.progressLabel)
        diskLayout.addWidget(self.diskProgress)
        diskLayout.addWidget(self.diskQuota)
        diskLayout.addWidget(self.spaceLabel)
        diskLayout.addWidget(self.dedicatedSpace)

        self.setLayout(diskLayout)

    def aggiorna(self):
        self.Sg_update_space.emit()

    def updateSpace(self, size):

        self.folderSize = size
        settings.update_quota_disco(self.dedicatedSpace.text())
        maxSize = settings.get_quota_disco()

        self.diskProgress.setRange(0, maxSize)
        self.diskProgress.setValue(self.folderSize)
        self.diskQuota.setText(
            f"{self.folderSize} su {self.convert_size(maxSize)}")

    @staticmethod
    def convert_size(size_bytes: int) -> str:
        """
        Method used to convert from byte to the biggest representation

        :param size_bytes:
        :return: a string with the number and the new numeric base
        """
        # TODO: Forse è da spostare
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

