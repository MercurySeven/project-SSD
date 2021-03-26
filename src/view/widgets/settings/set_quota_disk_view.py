from PySide6.QtWidgets import (QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)
from PySide6.QtCore import (Qt, Signal, Slot)
from PySide6.QtGui import (QIntValidator)

from src.model.settings_model import SettingsModel


class SetQuotaDiskView(QWidget):

    Sg_view_changed = Signal()

    def __init__(self, model: SettingsModel, parent=None):
        super(SetQuotaDiskView, self).__init__(parent)

        self._model = model

        self.setAccessibleName("InfoBox")

        self.title = QLabel()
        self.title.setText("Quota disco")
        self.title.setAccessibleName("Subtitle")

        # Barra riempimento disco
        self.progressLabel = QLabel()
        self.progressLabel.setText("Spazio occupato")
        self.progressLabel.setAccessibleName("Subtitle")

        self.diskProgress = QProgressBar()
        self.diskProgress.setFormat("")

        self.diskQuota = QLabel()

        # Modifica spazio dedicato
        self.spaceLabel = QLabel("Spazio dedicato")
        self.spaceLabel.setAccessibleName("Subtitle")

        self.dedicatedSpace = QLineEdit()
        self.dedicatedSpace.setValidator(QIntValidator())
        self.dedicatedSpace.returnPressed.connect(self.emit_changes)

        # layout
        disk_layout = QVBoxLayout()
        disk_layout.setAlignment(Qt.AlignLeft)
        disk_layout.addWidget(self.progressLabel)
        disk_layout.addWidget(self.diskProgress)
        disk_layout.addWidget(self.diskQuota)
        disk_layout.addWidget(self.spaceLabel)
        disk_layout.addWidget(self.dedicatedSpace)

        self.setLayout(disk_layout)
        self.Sl_model_changed()

    @Slot()
    def emit_changes(self):
        self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        new_max_quota = self._model.get_quota_disco()
        new_max_quota_raw = self._model.get_quota_disco_raw()
        value = self._model.get_size()
        self.diskQuota.setText(f"{value} su {new_max_quota}")
        self.dedicatedSpace.setText(str(new_max_quota_raw))
        self.diskProgress.setRange(0, new_max_quota_raw)
        self.diskProgress.setValue(value)
