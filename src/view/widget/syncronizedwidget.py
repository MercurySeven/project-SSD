from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QSizePolicy)
from model.directory import Directory

from view.widget.subwidget.filewidget import FileWidget
import settings


class SyncronizedWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SyncronizedWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.env_settings = QSettings()
        self.current_dir = Directory('', self.env_settings.value("sync_path"))
        self.listOfFileWidget = []
        for file in self.current_dir.files:
            self.listOfFileWidget.append(FileWidget(file.get_name(), file.get_creation_date(
            ), file.get_last_modified_date(), file.get_type(), file.get_size(), file.get_status()))

        self.header = FileWidget(
            'Nome', 'Creazione', 'Ultima Modifica', 'Tipo', 'Grandezza', 'Stato Sync')
        self.header.setAccessibleName('FileHeader')

        self.scrollArea = QScrollArea()
        self.scrollArea.setAccessibleName('FileScroll')
        # self.scrollArea.setStyleSheet("background-color:blue;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setLayout(QVBoxLayout())
        self.scrollArea.layout().setSpacing(0)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        self.fileWindow = QWidget(self)
        fileLayout = QVBoxLayout()
        fileLayout.setContentsMargins(0,0,0,0)
        # create layout

        layout.addWidget(self.header)
        for widget in self.listOfFileWidget:
            fileLayout.addWidget(widget)
            widget.setParent(self.fileWindow)
        self.fileWindow.setLayout(fileLayout)
        self.fileWindow.setParent(self.scrollArea)
        self.scrollArea.setWidget(self.fileWindow)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
