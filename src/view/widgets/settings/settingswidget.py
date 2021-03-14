from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton)

from .diskquota import DiskQuota
from .set_path_view import SetPathView
from model.widgets.settings import SetPathModel
from controllers.widgets.settings import SetPathController
import settings


class SettingsWidget(QWidget):

    # creating Signals
    Sg_policy_client = Signal()
    Sg_policy_manuale = Signal()
    Sg_dedicated_quota_changed = Signal()

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        self.setObjectName('Settings')

        # environment variables
        self.env_settings = QSettings()

        # widgets
        self.diskQuota = DiskQuota(self)

        # Titolo
        self.title = QLabel("Impostazioni", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName('Title')

        # Impostazioni path
        self.set_path_model = SetPathModel()
        self.set_path_controller = SetPathController(self.set_path_model)
        self.set_path_view = SetPathView(
            self.set_path_model, self.set_path_controller)

        # Impostazioni Priorità
        self.priorityLabel = QLabel(self)
        self.priorityLabel.setText(
            "Seleziona la politica di gestione dei conflitti")
        self.priorityLabel.setAccessibleName('Subtitle')

        self.radio_client = QRadioButton("Client")
        self.radio_client.setChecked(True)
        self.radio_client.clicked.connect(lambda: self.setPriority("Client"))

        self.radio_manuale = QRadioButton("Manuale")
        self.radio_manuale.clicked.connect(lambda: self.setPriority("Manuale"))

        # Impostazioni quota disco
        self.diskLabel = QLabel(self)
        self.diskLabel.setText("Quota disco")
        self.diskLabel.setAccessibleName('Subtitle')
        settings.check_file()

        self.diskQuota.Sg_dedicated_quota_changed.connect(
            self.__Sl_dedicated_quota_changed)

        # layout
        self.init_layout()

    def init_layout(self):

        path_layout = QHBoxLayout()
        path_layout.setAlignment(Qt.AlignLeft)

        radio_layout = QHBoxLayout()
        radio_layout.setAlignment(Qt.AlignLeft)
        radio_layout.addWidget(self.radio_client)
        radio_layout.addWidget(self.radio_manuale)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.set_path_view)
        layout.addWidget(self.priorityLabel)
        layout.addLayout(radio_layout)
        layout.addWidget(self.diskLabel)
        layout.addWidget(self.diskQuota)
        layout.addStretch()
        self.setLayout(layout)

    @Slot(int)
    def __Sl_dedicated_quota_changed(self, new_size: int) -> None:
        # aggiorno la quota dedicata
        settings.update_quota_disco(str(new_size))
        # aggiorno il widget
        self.Sl_update_used_quota(self.diskQuota.get_used_quota())

        # avviso che la quota dedicata è cambiato
        self.Sg_dedicated_quota_changed.emit()

    @Slot(int)
    def Sl_update_used_quota(self, size: int) -> None:
        max_size = settings.get_quota_disco()
        # maxSize = self.env_settings.value("Disk/quota")
        self.diskQuota.set_context((0, max_size), size)

    def setPriority(self, policy: str):
        if policy == "Client":
            self.Sg_policy_client.emit()
        elif policy == 'Manuale':
            self.Sg_policy_manuale.emit()
