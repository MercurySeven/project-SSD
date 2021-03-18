from PySide6.QtCore import (QSettings, QUrl)
from PySide6.QtGui import (QDesktopServices)
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton)
from src.view.layouts.flowlayout import FlowLayout
from src.view.widgets.filewidget import FileWidget


class FileSyncronizedWidget(QWidget):

    # creating Signals
    # TODO

    def __init__(self, parent=None):
        super(FileSyncronizedWidget, self).__init__(parent)

        self.env_settings = QSettings()
        self.list_of_file_widget = {}
        self.list_of_dirs_widget = {}

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
        # self.updateButton.clicked.connect(self.updateFiles)

        self.fileButton = QPushButton(self)
        self.fileButton.setText('Apri file manager')
        self.fileButton.clicked.connect(self.show_folder)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.updateButton)
        button_layout.addWidget(self.fileButton)

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

    def show_folder(self):
        path = QUrl.fromUserInput(self.env_settings.value("sync_path"))
        QDesktopServices.openUrl(path)

    def update_content(self, list_of_files: dict, list_of_dirs: dict) -> None:
        new_list_files = {k: list_of_files[k] for k in set(list_of_files) - set(self.list_of_file_widget)}
        # new_list_dirs = {
        # k: list_of_dirs[k] for k in set(list_of_dirs) - set(self.list_of_dirs_widget)
        # }
        for k in new_list_files:
            self.list_of_file_widget.update({
                new_list_files[k].get_name(): FileWidget(new_list_files[k])
            })
        for key in self.list_of_file_widget:
            widget = self.list_of_file_widget[key]
            self.fileLayout.addWidget(widget)
            widget.setParent(self.fileWindow)
        # TODO creazione widget per directory e completamento di questo ciclo
        # for k in new_list_dirs:
        #    self.list_of_dirs_widget.update({k.get_name(): })
