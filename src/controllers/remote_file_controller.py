from src.model.remote_file_model import RemoteFileModel
from src.model.settings_model import SettingsModel
from src.model.main_model import MainModel
from src.view.remote_file_view import RemoteFileView
from PySide2.QtCore import (Slot)


class RemoteFileController:
    def __init__(self, model: MainModel, view: RemoteFileView):
        self._model: RemoteFileModel = model.remote_file_model
        self.settings_model: SettingsModel = model.settings_model
        self._view = view
        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)
        # Connect per caricare il contenuto della cartella selezionata
        self._view.Sg_update_files_with_new_id.connect(self.Sl_update_files_with_new_id)
        # Connect per l'aggiunta di file alla whitelist
        self._view.Sg_add_sync_file.connect(self.Sl_add_sync_file)
        # Connect per la rimozione di file dalla whitelist
        self._view.Sg_remove_sync_file.connect(self.Sl_remove_sync_file)
        # Connect update dal model alla view
        self.settings_model.Sg_model_changed.connect(self._view.Sl_file_status_changed)

    @Slot(str)
    def Sl_update_files_with_new_id(self, id: str) -> None:
        self._model.set_current_node(id)

    @Slot(str)
    def Sl_add_sync_file(self, id: str) -> None:
        self.settings_model.add_id_to_sync_list(id)

    @Slot(str)
    def Sl_remove_sync_file(self, id: str) -> None:
        self.settings_model.remove_id_from_sync_list(id)
