from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QSizePolicy, QGridLayout, QPushButton)
from model.directory import Directory

from view.widget.subwidget.filewidget import FileWidget
from view.layouts.flowlayout import FlowLayout
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

        self.fileLayout = FlowLayout()

        # scroll area

        self.scrollArea = QScrollArea()
        self.scrollArea.setAccessibleName('FileScroll')

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        # contenitore per file

        self.fileWindow = QWidget(self)
        self.fileLayout.setContentsMargins(0,0,0,0)

        self.updateButton = QPushButton(self)
        self.updateButton.setText('Refresh')
        self.updateButton.clicked.connect(self.updateFiles)

        self.fileLayout.addWidget

        self.addFiles()

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.updateButton)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

    def updateFiles(self):

        for i in reversed(range(self.fileLayout.count())): 
            self.fileLayout.itemAt(i).widget().deleteLater()

        self.current_dir = Directory('', self.env_settings.value("sync_path"))

        self.current_dir.files.clear()

        self.current_dir.update_list_of_files()

        self.addFiles()

    def addFiles(self):

        self.listOfFileWidget.clear()

        for file in self.current_dir.files:
            self.listOfFileWidget.append(FileWidget(file.get_name(), file.get_creation_date(
            ), file.get_last_modified_date(), file.get_type(), file.get_size(), file.get_status()))


        for widget in self.listOfFileWidget:
            self.fileLayout.addWidget(widget)
            widget.setParent(self.fileWindow)

        

