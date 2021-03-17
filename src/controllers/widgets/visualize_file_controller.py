from PySide6.QtCore import (Slot, Signal)
from PySide6.QtWidgets import (QWidget)
from src.model.files_model import FilesModel


class VisualizeFileController:
    update_view = Signal(dict)

    def __init__(self, view: QWidget, model: FilesModel):
        self.model = model
        self.view = view

    @Slot()
    def update_visualization(self) -> None:
        list_of_files, list_of_dirs = self.model.update_view("ciao")
        self.view.update_view(list_of_files, list_of_dirs)
