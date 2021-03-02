from PySide6.QtWidgets import (
    QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)
from PySide6.QtGui import QIntValidator

import os
import math

from settings import Settings

from PySide6.QtCore import Qt


def get_size(start_path: str = '.') -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


class diskQuota(QWidget):

    def __init__(self, parent=None):
        super(diskQuota, self).__init__(parent)

        self.settings = Settings()

        self.setAccessibleName('InfoBox')

        folderSize = get_size(self.settings.get_path())
        maxSize = self.settings.get_quota_disco()

        # Barra riempimento disco

        self.progressLabel = QLabel(self)
        self.progressLabel.setText('Spazio occupato')
        self.progressLabel.setAccessibleName('Subtitle')

        self.diskProgress = QProgressBar()
        self.diskProgress.setFormat('')
        self.diskProgress.setRange(0, maxSize)
        self.diskProgress.setValue(folderSize)
        self.diskQuota = QLabel()
        self.diskQuota.setText(
            f"{folderSize} su {self.convert_size(maxSize)}")

        # Modifica spazio dedicato

        self.spaceLabel = QLabel('Spazio dedicato')
        self.spaceLabel.setAccessibleName('Subtitle')

        self.dedicatedSpace = QLineEdit()
        onlyInt = QIntValidator()
        self.dedicatedSpace.setValidator(onlyInt)
        self.dedicatedSpace.setText(str(maxSize))

        self.dedicatedSpace.returnPressed.connect(self.updateSpace)

        diskLayout = QVBoxLayout()
        diskLayout.setAlignment(Qt.AlignLeft)
        diskLayout.addWidget(self.progressLabel)
        diskLayout.addWidget(self.diskProgress)
        diskLayout.addWidget(self.diskQuota)
        diskLayout.addWidget(self.spaceLabel)
        diskLayout.addWidget(self.dedicatedSpace)

        self.setLayout(diskLayout)

    def updateSpace(self):

        folderSize = get_size(self.settings.get_path())
        self.settings.update_quota_disco(self.dedicatedSpace.text())
        maxSize = self.settings.get_quota_disco()

        self.diskProgress.setRange(0, maxSize)
        self.diskProgress.setValue(folderSize)
        self.diskQuota.setText(
            f"{folderSize} su {self.convert_size(maxSize)}")

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
