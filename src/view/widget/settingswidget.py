from PySide6.QtCore import (Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QFileDialog, QRadioButton)

from src.settings import Settings


class SettingsWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        # environment variables
        self.settings = QSettings(self)
        self.mysettings = Settings()

        self.setObjectName('Settings')

        # Titolo
        self.title = QLabel("Impostazioni", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName('Title')

        # Impostazioni path
        self.titoloPath = QLabel(self)
        self.titoloPath.setText("Cartella da sincronizzare")
        self.titoloPath.setAccessibleName('Subtitle')

        self.path_label = QLabel(self)
        self.updatePathText(self.settings.value("sync_path"))

        self.changePathButton = QPushButton('Cambia PATH', self)
        self.changePathButton.setMaximumWidth(150)

        # Impostazioni Priorità
        self.priorityLabel = QLabel(self)
        self.priorityLabel.setText(
            "Seleziona a quale archivio dare la priorità")
        self.priorityLabel.setAccessibleName('Subtitle')

        self.radioLocal = QRadioButton("Locale")
        self.radioLocal.setChecked(True)
        self.radioLocal.clicked.connect(lambda: self.setPriority(
            self.radioLocal))

        self.radioRemote = QRadioButton("Remoto")
        self.radioRemote.clicked.connect(lambda: self.setPriority(
            self.radioRemote))

        # connect
        self.changePathButton.clicked.connect(self.setPath)

        # create layout
        pathLayout = QHBoxLayout()
        pathLayout.setAlignment(Qt.AlignLeft)
        pathLayout.addWidget(self.path_label)
        pathLayout.addWidget(self.changePathButton)

        radioLayout = QHBoxLayout()
        radioLayout.setAlignment(Qt.AlignLeft)
        radioLayout.addWidget(self.radioLocal)
        radioLayout.addWidget(self.radioRemote)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.titoloPath)
        layout.addLayout(pathLayout)
        layout.addWidget(self.priorityLabel)
        layout.addLayout(radioLayout)
        layout.addStretch()
        self.setLayout(layout)

    def updatePathText(self, new_path: str) -> None:
        self.path_label.setText(new_path)

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
                self.settings.update_path(sync_path[0])
                self.updatePathText(self.settings.get_path())
                print("Nuova directory impostata: " + self.settings.get_path())

    def setPriority(self, b):
        if(b.text() == 'Locale'):
            print("locale")
        else:
            print("remoto")
