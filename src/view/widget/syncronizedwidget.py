from PySide6.QtCore import (Signal, Slot, Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QSizePolicy)
from model.directory import Directory

from view.widget.subwidget.filewidget import FileWidget
from settings import Settings


class SyncronizedWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SyncronizedWidget, self).__init__(parent)

        self.settings = Settings()
        layout = QVBoxLayout()
        self.current_dir = Directory('', self.settings.get_path())
        self.listOfFileWidget = []
        for file in self.current_dir.files:
            self.listOfFileWidget.append(FileWidget(file.getName(), file.getCreationDate(), file.getLastModifiedDate(), file.getType(), file.getSize(), file.getStatus()))
        
        self.header = FileWidget('Nome', 'Creazione', 'Ultima Modifica', 'Tipo', 'Grandezza', 'Stato Sync')
        self.header.setAccessibleName('FileHeader')

        self.scrollArea = QScrollArea()
        self.scrollArea.setAccessibleName('FileScroll')
        # self.scrollArea.setStyleSheet("background-color:blue;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        self.fileWindow = QWidget(self)
        fileLayout = QVBoxLayout()
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

