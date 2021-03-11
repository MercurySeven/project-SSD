from PySide6.QtCore import (QSettings, QUrl)
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton)
from model import Directory

from PySide6.QtGui import QDesktopServices

from view.widgets.subwidget.filewidget import FileWidget
from view.layouts.flowlayout import FlowLayout


class SyncronizedWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(SyncronizedWidget, self).__init__(parent)

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
        self.fileLayout.setContentsMargins(0, 0, 0, 0)

        self.updateButton = QPushButton(self)
        self.updateButton.setText('Refresh')
        self.updateButton.clicked.connect(self.updateFiles)

        self.fileButton = QPushButton(self)
        self.fileButton.setText('Apri file manager')
        self.fileButton.clicked.connect(self.showFolder)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.updateButton)
        button_layout.addWidget(self.fileButton)

        self.fileLayout.addWidget

        self.addFiles()

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
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

        for _file in self.current_dir.files:
            self.listOfFileWidget.append(FileWidget(_file))

        for widget in self.listOfFileWidget:
            self.fileLayout.addWidget(widget)
            widget.setParent(self.fileWindow)

    def showFolder(self):
        QDesktopServices.openUrl(
            QUrl(self.env_settings.value("sync_path"), QUrl.TolerantMode))
