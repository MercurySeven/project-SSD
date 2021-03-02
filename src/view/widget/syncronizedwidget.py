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

        scrollArea = QScrollArea()
        scrollArea.setAccessibleName('FileScroll')
        scrollArea.setWidgetResizable(True)
        scrollArea.horizontalScrollBar().setEnabled(False)

        fileWindow = QWidget(self)
        fileLayout = QVBoxLayout()
        # create layout

        layout.addWidget(self.header)
        for widget in self.listOfFileWidget:
            fileLayout.addWidget(widget)
            widget.setAccessibleName('File')
        fileWindow.setLayout(fileLayout)
        fileWindow.setParent(scrollArea)
        scrollArea.setWidget(fileWindow)
        layout.addWidget(scrollArea)
        self.setLayout(layout)

