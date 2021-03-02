from PySide6.QtCore import (Signal, Slot, Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)
from view.widget.watchwidget import WatchWidget
from model.directory import Directory

from .subwidget.filewidget import FileWidget
from settings import Settings
class SyncronizedWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SyncronizedWidget, self).__init__(parent)

        self.label = QLabel("<TODO Syncronized here>", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.settings = Settings()
        self.layout = QVBoxLayout(self)
        self.current_dir = Directory('', self.settings.get_path())
        self.listOfFileWidget = []
        for file in self.current_dir.files:
            self.listOfFileWidget.append(FileWidget(file.getName(), file.getCreationDate(), file.getLastModifiedDate(), file.getType(), file.getSize(), file.getStatus()))

        #for widget in self.listOfFileWidget:
        #    self.layout.addWidget(widget)
        # self.setLayout(self.layout)
        # create layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # self.setLayout(layout)

