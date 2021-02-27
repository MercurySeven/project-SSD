from PySide6.QtCore import (Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QRadioButton)


class SettingsWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        # environment variables
        self.settings = QSettings(self)

        self.title = QLabel("SETTINGS", self)
        self.title.setAlignment(Qt.AlignCenter)

        self.path_label = QLabel(self)
        self.updatePathText(self.settings.value("sync_path"))
        self.changePathButton = QPushButton('Cambia PATH', self)

        self.priorityLabel = QLabel(self)
        self.priorityLabel.setText(
            "Seleziona a quale archivio dare la priorità")

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
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.path_label)
        layout.addWidget(self.changePathButton)
        layout.addWidget(self.priorityLabel)
        layout.addWidget(self.radioLocal)
        layout.addWidget(self.radioRemote)
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
                self.settings.setValue("sync_path", sync_path[0])
                self.updatePathText(self.settings.value("sync_path"))
                print("Nuova directory impostata: " +
                      self.settings.value("sync_path"))
                self.settings.sync()  # save

    def setPriority(self, b):
        if(b.text() == 'Locale'):
            print("locale")
        else:
            print("remoto")
