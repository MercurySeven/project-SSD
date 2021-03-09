from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QFileDialog, QRadioButton)

from .diskquota import DiskQuota
import settings


class SettingsWidget(QWidget):

    # creating Signals
    Sg_path_changed = Signal()
    Sg_policy_lastUpdate = Signal()
    Sg_policy_Client = Signal()
    Sg_policy_Server = Signal()
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
            "Seleziona a quale archivio dare la priorità")
        self.priorityLabel.setAccessibleName('Subtitle')

        self.radioLocal = QRadioButton("Locale")
        self.radioLocal.clicked.connect(lambda: self.setPriority(
            self.radioLocal))

        self.radioRemote = QRadioButton("Remoto")
        self.radioRemote.clicked.connect(lambda: self.setPriority(
            self.radioRemote))

        self.radioLastUpdate = QRadioButton("lastUpdate")
        self.radioLastUpdate.setChecked(True)
        self.radioLastUpdate.clicked.connect(lambda: self.setPriority(
            self.radioLastUpdate))

        # Impostazioni quota disco
        self.diskLabel = QLabel(self)
        self.diskLabel.setText(
            "Quota disco")
        self.diskLabel.setAccessibleName('Subtitle')
        settings.check_file()
        
        self.diskQuota.Sg_dedicated_quota_changed.connect(
            self.__Sl_dedicated_quota_changed)

        # layout
        self.init_layout()

    def init_layout(self):

        pathLayout = QHBoxLayout()
        pathLayout.setAlignment(Qt.AlignLeft)
        pathLayout.addWidget(self.path_label)
        pathLayout.addWidget(self.changePathButton)

        radioLayout = QHBoxLayout()
        radioLayout.setAlignment(Qt.AlignLeft)
        radioLayout.addWidget(self.radioLocal)
        radioLayout.addWidget(self.radioRemote)
        radioLayout.addWidget(self.radioLastUpdate)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.titoloPath)
        layout.addLayout(pathLayout)
        layout.addWidget(self.priorityLabel)
        layout.addLayout(radioLayout)
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
        maxSize = settings.get_quota_disco()
        # maxSize = self.env_settings.value("Disk/quota")
        self.diskQuota.set_context((0, maxSize), size)

    @Slot()
    def setPath(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        # L'utente non ha selezionato la cartella
        if dialog.exec_():
            sync_path = dialog.selectedFiles()
            if (len(sync_path) == 1):
                self.env_settings.setValue("sync_path", sync_path[0])
                self.env_settings.sync()
                self.updatePathText()

                self.Sg_path_changed.emit()

    def setPriority(self, b):
        if b.text() == 'Locale':
            self.Sg_policy_Client.emit()
        elif b.text() == 'Remoto' :
            self.Sg_policy_Server.emit()
        elif b.text() == 'lastUpdate':
            self.Sg_policy_lastUpdate.emit()
