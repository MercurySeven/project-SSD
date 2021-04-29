from PySide6.QtCore import (QSettings, Slot, Qt, Signal)
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QScrollArea, QPushButton, QLabel)

from src.model.remote_file_model import RemoteFileModel
from src.view.layouts.flowlayout import FlowLayout
from src.view.widgets.directory_widget import DirectoryWidget
from src.view.widgets.file_widget import FileWidget


class RemoteView(QWidget):
    Sg_update_files_with_new_path = Signal(str)

    def __init__(self, model: RemoteFileModel, parent=None):
        super(RemoteView, self).__init__(parent)

        self.env_settings = QSettings()
        self._model = model

        self.title = QLabel("File remoti", self)
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

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.Sl_model_changed()

    @Slot()
    def Sl_model_changed(self) -> None:
        list_of_files, list_of_dirs = self._model.get_data()

        for i in reversed(range(self.fileLayout.count())):
            self.fileLayout.itemAt(i).widget().setParent(None)
        for i in list_of_dirs:
            self.fileLayout.addWidget(DirectoryWidget(i, self))
        for i in list_of_files:
            self.fileLayout.addWidget(FileWidget(i))

    @Slot(str)
    def Sl_update_files_with_new_path(self, path: str) -> None:
        self.Sg_update_files_with_new_path.emit(path)