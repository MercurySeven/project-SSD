from src.model.file_model import FileModel
from src.view.file_view import FileView
from PySide6.QtCore import (Slot)


class FileController:
    def __init__(self, model: FileModel, view: FileView):
        self._model = model
        self._view = view
        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)
        self._view.show_path_button.clicked.connect(self._view.Sl_show_path_button_clicked)
        # Connect per caricare il contenuto della cartella selezionata
        self._view.Sg_update_files_with_new_path.connect(self.Sl_update_files_with_new_path)

    @Slot(str)
    def Sl_update_files_with_new_path(self, path: str) -> None:
        self._model.set_current_node(path)

    @Slot(str, bool)
    def Sl_toggle_files_update(self, file_path: str, is_sync: bool) -> None:
        self._view.toggle_files_update(file_path, is_sync)
