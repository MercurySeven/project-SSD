from PySide6.QtCore import (Slot)

from src.model.files_model import FilesModel
from src.view.file_view import FileView


class FileController:
    def __init__(self, model: FilesModel, view: FileView):
        self._model = model
        self._view = view
        self._model.Sg_model_changed.connect(self._view.Sl_update_list_files)
        self._view.updateButton.clicked.connect(self._model.Sl_update_model)

    @Slot()
    def switch_to_files(self) -> None:
        list_of_files, list_of_dirs = self._model.update_view()
        self._view.update_view(list_of_files, list_of_dirs)
