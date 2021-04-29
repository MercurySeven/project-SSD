from src.model.remote_file_model import RemoteFileModel
from src.view.remote_file_view import RemoteFileView
from PySide6.QtCore import (Slot)


class RemoteFileController:
    def __init__(self, model: RemoteFileModel, view: RemoteFileView):
        self._model = model
        self._view = view
        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)
        # Connect per caricare il contenuto della cartella selezionata
        self._view.Sg_update_files_with_new_path.connect(self.Sl_update_files_with_new_path)

    @Slot(str)
    def Sl_update_files_with_new_path(self, path: str) -> None:
        self._model.set_current_node(path)
