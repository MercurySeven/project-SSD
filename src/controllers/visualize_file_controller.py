from PySide6.QtCore import (Slot)

from src.model.files_model import FilesModel
from src.view.file_synchronized_widget import FileSyncronizedWidget


class VisualizeFileController:
    def __init__(self, view: FileSyncronizedWidget, model: FilesModel):
        self.model = model
        self.view = view
        self.model.Sg_model_changed.connect(self.view.Sl_update_list_files)

    @Slot()
    def switch_to_files(self) -> None:
        list_of_files, list_of_dirs = self.model.update_view()
        self.view.update_view(list_of_files, list_of_dirs)
