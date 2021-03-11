from PySide6.QtWidgets import (
    QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)
from PySide6.QtCore import (Signal, Slot)
from PySide6.QtGui import (QIntValidator)

import math

from PySide6.QtCore import Qt


class DiskQuota(QWidget):

    Sg_dedicated_quota_changed = Signal(int)

    def __init__(self, parent=None):
        super(DiskQuota, self).__init__(parent)

        self.setAccessibleName('InfoBox')

        # Barra riempimento disco
        self.progressLabel = QLabel(self)
        self.progressLabel.setText('Spazio occupato')
        self.progressLabel.setAccessibleName('Subtitle')

        self.diskProgress = QProgressBar(self)
        self.diskProgress.setFormat('')

        self.diskQuota = QLabel(self)

        # Modifica spazio dedicato
        self.spaceLabel = QLabel('Spazio dedicato', self)
        self.spaceLabel.setAccessibleName('Subtitle')

        self.dedicatedSpace = QLineEdit(self)
        self.dedicatedSpace.setValidator(QIntValidator())
        self.dedicatedSpace.returnPressed.connect(self.emit_changes)

        # init value
        self.set_context((0, 0), 0)

        # layout
        self.init_layout()

    def init_layout(self):

        disk_layout = QVBoxLayout()
        disk_layout.setAlignment(Qt.AlignLeft)
        disk_layout.addWidget(self.progressLabel)
        disk_layout.addWidget(self.diskProgress)
        disk_layout.addWidget(self.diskQuota)
        disk_layout.addWidget(self.spaceLabel)
        disk_layout.addWidget(self.dedicatedSpace)

        self.setLayout(disk_layout)

    @Slot()
    def emit_changes(self):
        new_size = int(self.dedicatedSpace.text())
        self.Sg_dedicated_quota_changed.emit(new_size)

    def get_used_quota(self) -> int:
        return self.diskProgress.value()

    def set_context(self, progress_range: tuple[int, int], value: int) -> None:
        """
        Parameters
        ----------
        progress_range : tuple(int, int)
            the range of the progress bar, range[0] = min, range[1] = max
        value : int
            actual value of the quota
        """
        try:
            _min, _max = progress_range
            self.diskProgress.setRange(_min, _max)
            self.diskProgress.setValue(value)
            self.diskQuota.setText(
                f"{value} su {self.convert_size(_max)}")
            self.dedicatedSpace.setText(str(_max))
        except Exception as e:
            # TODO migliorare la gestione delle eccezzioni
            raise Exception(f"setting DiskQuota context failed: {str(e)}")

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
