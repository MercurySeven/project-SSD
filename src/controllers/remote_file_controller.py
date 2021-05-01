from src.model.remote_file_model import RemoteFileModel
from src.view.remote_file_view import RemoteFileView
from PySide6.QtCore import (Slot)
from src import settings


class RemoteFileController:
    def __init__(self, model: RemoteFileModel, view: RemoteFileView):
        self._model = model
        self._view = view
        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)
        # Connect per caricare il contenuto della cartella selezionata
        self._view.Sg_update_files_with_new_id.connect(self.Sl_update_files_with_new_id)
        # Connect per l'aggiunta di folder alla whitelist
        self._view.Sg_add_sync_folder.connect(self.Sl_add_sync_folder)
        # Connect per la rimozione di folder dalla whitelist
        self._view.Sg_remove_sync_folder.connect(self.Sl_remove_sync_folder)

    @Slot(str)
    def Sl_update_files_with_new_id(self, id: str) -> None:
        self._model.set_current_node(id)

    @Slot(str)
    def Sl_add_sync_folder(self, id: str) -> None:
        settings.add_id_to_sync_list(id)

    @Slot(str)
    def Sl_remove_sync_folder(self, id: str) -> None:
        settings.remove_id_from_sync_list(id)
