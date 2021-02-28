from PySide6.QtCore import (Signal, Slot, Qt)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QProgressBar, QLineEdit)
from PySide6.QtGui import QIntValidator
from settings import Settings
import os


def get_size(start_path: str = '.') -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


class DiskQuotaWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(DiskQuotaWidget, self).__init__(parent)

        # Titolo pagina
        self.title = QLabel("Quota disco", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName('Title')

        # Spazio utilizzato
        self.diskLabel = QLabel('Spazio utilizzato')
        self.diskLabel.setAlignment(Qt.AlignLeft)
        self.diskLabel.setAccessibleName('Subtitle')

        # Percentuale spazio
        self.diskView = QWidget()
        self.diskView.setAccessibleName('InfoBox')

        self.settings = Settings()

        folderSize = get_size(self.settings.get_path())
        maxSize = int(self.settings.get_quota_disco())

        self.diskView.diskProgress = QProgressBar()
        self.diskView.diskProgress.setFormat('')
        self.diskView.diskProgress.setRange(0, maxSize)
        self.diskView.diskProgress.setValue(folderSize)

        self.diskView.diskQuota = QLabel()
        self.diskView.diskQuota.setText(
            str(folderSize) + ' su ' + str(maxSize))

        diskLayout = QVBoxLayout()
        diskLayout.addWidget(self.diskView.diskProgress)
        diskLayout.addWidget(self.diskView.diskQuota)

        self.diskView.setLayout(diskLayout)

        # Quantità spazio dedicato

        self.spaceLabel = QLabel('Spazio dedicato')
        self.spaceLabel.setAlignment(Qt.AlignLeft)
        self.spaceLabel.setAccessibleName('Subtitle')

        # Spazio modificabile

        self.spaceView = QWidget()
        self.spaceView.setAccessibleName('InfoBox')

        self.spaceView.dedicatedSpace = QLineEdit()
        onlyInt = QIntValidator()
        self.spaceView.dedicatedSpace.setValidator(onlyInt)
        self.spaceView.dedicatedSpace.setText(str(maxSize))

        self.spaceView.dedicatedSpace.returnPressed.connect(self.updateSpace)

        spaceLayout = QVBoxLayout()
        spaceLayout.addWidget(self.spaceView.dedicatedSpace)

        self.spaceView.setLayout(spaceLayout)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.diskLabel)
        layout.addWidget(self.diskView)
        layout.addWidget(self.spaceLabel)
        layout.addWidget(self.spaceView)
        layout.addStretch()
        self.setLayout(layout)

    def updateSpace(self):
        folderSize = get_size(self.settings.get_path())
        self.settings.update_quota_disco(self.spaceView.dedicatedSpace.text())
        maxSize = self.settings.get_quota_disco()
        print(maxSize)

        self.diskView.diskProgress.setRange(0, maxSize)
        self.diskView.diskProgress.setValue(folderSize)
        self.diskView.diskQuota.setText(
            str(folderSize) + ' su ' + str(maxSize))
