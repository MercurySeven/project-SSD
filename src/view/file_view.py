import os

from PySide6.QtCore import (QSettings, QUrl, Slot, Qt, Signal)
from PySide6.QtGui import (QDesktopServices)
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton, QLabel)

from src.model.file_model import FileModel
from src.view.layouts.flowlayout import FlowLayout
from src.view.widgets.local_directory_widget import LocalDirectoryWidget
from src.view.widgets.local_file_widget import LocalFileWidget


class FileView(QWidget):
    Sg_update_files_with_new_path = Signal(str)

    def __init__(self, model: FileModel, parent=None):
        super(FileView, self).__init__(parent)

        self.env_settings = QSettings()
        self._model = model

        self.title = QLabel("File locali", self)
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

        self.show_path_button = QPushButton("Apri file manager", self)
        self.force_sync_button = QPushButton("Sincronizza ora", self)

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.force_sync_button)
        header_layout.addWidget(self.show_path_button)

        layout = QVBoxLayout()
        layout.addLayout(header_layout)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.Sl_model_changed()

    @Slot()
    def Sl_show_path_button_clicked(self) -> None:
        path = QUrl.fromUserInput(self.env_settings.value("sync_path"))
        QDesktopServices.openUrl(path)

    @Slot()
    def Sl_model_changed(self) -> None:
        list_of_files, list_of_dirs = self._model.get_data()

        for i in reversed(range(self.fileLayout.count())):
            self.fileLayout.itemAt(i).widget().setParent(None)
        for i in list_of_dirs:
            self.fileLayout.addWidget(LocalDirectoryWidget(i, self))
        for i in list_of_files:
            self.fileLayout.addWidget(LocalFileWidget(i))

    @Slot(str)
    def Sl_update_files_with_new_path(self, path: str) -> None:
        self.Sg_update_files_with_new_path.emit(path)

    def toggle_files_update(self, file_path: str) -> None:
        for widget in self.fileLayout._item_list:
            if type(widget.wid) == LocalFileWidget:
                if os.path.samefile(widget.wid.path, file_path):
                    widget.wid.toggle()
