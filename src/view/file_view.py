from PySide6.QtCore import (QSettings, QUrl, Slot, Qt, Signal)
from PySide6.QtGui import (QDesktopServices)
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton, QLabel)

from src.model.file_model import FileModel
from src.model.widgets.directory import Directory
from src.model.widgets.file import File
from src.view.layouts.flowlayout import FlowLayout
from src.view.widgets.directory_widget import DirectoryWidget
from src.view.widgets.file_widget import FileWidget


class FileView(QWidget):
    Sg_update_files_with_new_path = Signal(str)

    def __init__(self, model: FileModel, parent=None):
        super(FileView, self).__init__(parent)

        self.env_settings = QSettings()
        self._model = model

        self.title = QLabel("File sincronizzati", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setAccessibleName("FileScroll")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        # contenitore per file
        self.fileWindow = QWidget(self)
        self.fileLayout = FlowLayout()
        self.fileLayout.setContentsMargins(0, 0, 0, 0)

        self.refresh_button = QPushButton(self)
        self.refresh_button.setText("Refresh")

        self.show_path_button = QPushButton(self)
        self.show_path_button.setText("Apri file manager")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.show_path_button)

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addLayout(button_layout)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.Sl_model_changed()

    @Slot()
    def Sl_show_path_button_clicked(self) -> None:
        path = QUrl.fromUserInput(self.env_settings.value("sync_path"))
        QDesktopServices.openUrl(path)

    def update_content(self, list_of_files: list[File], list_of_dirs: list[Directory]) -> None:
        for i in reversed(range(self.fileLayout.count())):
            self.fileLayout.itemAt(i).widget().setParent(None)
        for i in list_of_dirs:
            self.fileLayout.addWidget(DirectoryWidget(i, self))
        for i in list_of_files:
            self.fileLayout.addWidget(FileWidget(i))

    @Slot()
    def Sl_model_changed(self) -> None:
        """metodo chiamato dal notify del modello quando questo si aggiorna"""
        list_of_files, list_of_dirs = self._model.get_data()
        self.update_content(list_of_files, list_of_dirs)

    @Slot(str)
    def Sl_update_files_with_new_path(self, path: str) -> None:
        self.Sg_update_files_with_new_path.emit(path)
