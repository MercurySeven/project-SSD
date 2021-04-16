from PySide6.QtCore import (Qt, Signal, Slot)
from PySide6.QtGui import (QIntValidator)
from PySide6.QtWidgets import (QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)

from src.model.settings_model import SettingsModel


class SetQuotaDiskWidget(QWidget):

    Sg_view_changed = Signal()

    def __init__(self, model: SettingsModel, parent=None):
        super(SetQuotaDiskWidget, self).__init__(parent)

        self._model = model

        self.setAccessibleName("InfoBox")

        self.title = QLabel()
        self.title.setText("Quota disco")
        self.title.setAccessibleName("Subtitle")

        # Barra riempimento disco
        self.progress_label = QLabel()
        self.progress_label.setText("Spazio occupato")
        self.progress_label.setAccessibleName("Subtitle")

        self.disk_progress = QProgressBar()
        self.disk_progress.setFormat("")

        self.disk_quota = QLabel()

        # Modifica spazio dedicato
        self.spaceLabel = QLabel("Spazio dedicato")
        self.spaceLabel.setAccessibleName("Subtitle")

        self.dedicated_space = QLineEdit()
        self.dedicated_space.setValidator(QIntValidator())
        self.dedicated_space.returnPressed.connect(self.Sl_dedicated_space_changed)

        # layout
        disk_layout = QVBoxLayout()
        disk_layout.setAlignment(Qt.AlignLeft)
        disk_layout.addWidget(self.progress_label)
        disk_layout.addWidget(self.disk_progress)
        disk_layout.addWidget(self.disk_quota)
        disk_layout.addWidget(self.spaceLabel)
        disk_layout.addWidget(self.dedicated_space)

        self.setLayout(disk_layout)
        self.Sl_model_changed()

    @Slot()
    def Sl_dedicated_space_changed(self):
        self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        new_max_quota = self._model.get_quota_disco()
        new_max_quota_raw = self._model.get_quota_disco_raw()
        value = self._model.convert_size(self._model.get_size())
        self.disk_quota.setText(f"{value} su {new_max_quota}")
        self.dedicated_space.setText(str(new_max_quota_raw))
        self.disk_progress.setRange(0, new_max_quota_raw)
        self.disk_progress.setValue(self._model.get_size())
