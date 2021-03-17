from PySide6.QtCore import (QSettings, Signal, Slot)
from  src.model.file import File
from src.model.directory import Directory
from src.model.widgets.settings_model import SettingsModel
from typing import Tuple

class FilesModel:
    update_view_signal = Signal(dict)
    def __init__(self):
        self.settings = QSettings()
        self.base_dir = Directory("root_dir", self.settings.value("sync_path"))

    # per ora ritorna solamente il contenuto del primo livello della directory
    # TODO ampliare la ricerca di una cartella e di un file

    def update_view(self, path: str) -> Tuple[dict, dict]:
        list_of_files = self.base_dir.files
        list_of_dirs = self.base_dir.dirs
        return list_of_files, list_of_dirs

