from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget, QLineEdit)


class SettingsWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        # environment variables
        self.settings = QSettings(self)

        self.title = QLabel("SETTINGS", self)
        self.title.setAlignment(Qt.AlignCenter)

        self.path_label = QLabel("Path")
        self.path_edit = QLineEdit(self.settings.value("sync/path"), self)

        # connect
        self.path_edit.textChanged.connect(self.setPath)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_edit)
        self.setLayout(layout)

    @Slot()
    def setPath(self):
        new_path = self.path_edit.text()
        self.settings.setValue("sync/path", new_path)
        self.settings.sync()
        print(f"new sync path {new_path}")  # debug
