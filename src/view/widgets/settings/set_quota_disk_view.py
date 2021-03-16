from PySide6.QtWidgets import (
    QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)
from PySide6.QtCore import (Qt, Signal, Slot)
from PySide6.QtGui import (QIntValidator)

from src.model.widgets.settings_model import SettingsModel
from src.controllers.widgets.settings.set_quota_disk_controller import SetQuotaDiskController


class SetQuotaDiskView(QWidget):

    Sg_dedicated_quota_changed = Signal(int)

    def __init__(self,
                 model: SettingsModel,
                 controller: SetQuotaDiskController,
                 parent=None):
        super(SetQuotaDiskView, self).__init__(parent)

        self._model = model
        self._controller = controller

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

        self._model.Sg_model_changed.connect(lambda: self.Sl_model_changed())
        self.Sg_dedicated_quota_changed.connect(
            self._controller.Sl_change_quota_disco)

    @Slot()
    def emit_changes(self):
        new_size = int(self.dedicatedSpace.text())
        self.Sg_dedicated_quota_changed.emit(new_size)

    @Slot()
    def Sl_model_changed(self):
        new_max_quota = self._model.get_quota_disco()
        new_max_quota_raw = self._model.get_quota_disco_raw()
        value = self._model.get_size()
        self.diskQuota.setText(f"{value} su {new_max_quota}")
        self.dedicatedSpace.setText(str(new_max_quota_raw))
        self.diskProgress.setRange(0, new_max_quota_raw)
        self.diskProgress.setValue(value)
