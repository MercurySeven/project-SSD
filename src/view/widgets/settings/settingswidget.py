from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QFileDialog, QRadioButton)

from .diskquota import DiskQuota
import settings


class SettingsWidget(QWidget):

    # creating Signals
    Sg_path_changed = Signal()
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
        self.titoloPath = QLabel(self)
        self.titoloPath.setText("Cartella da sincronizzare")
        self.titoloPath.setAccessibleName('Subtitle')

        self.path_label = QLabel(self)
        self.path_label.setEnabled(False)
        self.updatePathText()

        self.changePathButton = QPushButton('Cambia', self)
        self.changePathButton.setMaximumWidth(150)

        # connect
        self.changePathButton.clicked.connect(self.setPath)

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
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.changePathButton)

        radio_layout = QHBoxLayout()
        radio_layout.setAlignment(Qt.AlignLeft)
        radio_layout.addWidget(self.radio_client)
        radio_layout.addWidget(self.radio_manuale)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.titoloPath)
        layout.addLayout(path_layout)
        layout.addWidget(self.priorityLabel)
        layout.addLayout(radio_layout)
        layout.addWidget(self.diskLabel)
        layout.addWidget(self.diskQuota)
        layout.addStretch()
        self.setLayout(layout)

    def updatePathText(self) -> None:
        self.path_label.setText(self.env_settings.value("sync_path"))

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

    @Slot()
    def setPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        if dialog.exec_():
            sync_path = dialog.selectedFiles()
            if (len(sync_path) == 1):
                self.env_settings.setValue("sync_path", sync_path[0])
                self.env_settings.sync()
                self.updatePathText()

                self.Sg_path_changed.emit()

    def setPriority(self, policy: str):
        if policy == "Client":
            self.Sg_policy_client.emit()
        elif policy == 'Manuale':
            self.Sg_policy_manuale.emit()
