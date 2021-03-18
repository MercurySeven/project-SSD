from typing import Tuple

from PySide6.QtCore import (QSettings, Signal)

from src.model.directory import Directory


class FilesModel:
    notify_changes = Signal(dict, dict)

    def __init__(self):
        self.settings = QSettings()
        self.base_dir = Directory("root_dir", self.settings.value("sync_path"))
    # per ora ritorna solamente il contenuto del primo livello della directory
    # TODO ampliare la ricerca di una cartella e di un file

    def update_view(self) -> Tuple[dict, dict]:
        list_of_files = self.base_dir.files
        list_of_dirs = self.base_dir.dirs
        return list_of_files, list_of_dirs

    # def notify_view_of_changes(self):