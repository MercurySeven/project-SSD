from PySide6.QtCore import (Slot, Signal)
from PySide6.QtWidgets import (QWidget)

from src.model.files_model import FilesModel


class VisualizeFileController:
    switch_to_files = Signal(dict)

    def __init__(self, view: QWidget, model: FilesModel):
        self.model = model
        self.view = view
        
    @Slot()
    def switch_to_files(self) -> None:
        list_of_files, list_of_dirs = self.model.update_view()
        self.view.update_view(list_of_files, list_of_dirs)
