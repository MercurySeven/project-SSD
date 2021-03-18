from typing import Tuple

from PySide6.QtCore import (QSettings, Signal, QObject)

from src.model.directory import Directory


class FilesModel(QObject):
    notify_changes = Signal()

    def __init__(self):
        super(FilesModel, self).__init__()
        self.settings = QSettings()
        self.base_dir = Directory("root_dir", self.settings.value("sync_path"))
    # per ora ritorna solamente il contenuto del primo livello della directory
    # TODO ampliare la ricerca di una cartella e di un file

    def update_model(self) -> None:
        self.base_dir.update_list_of_content()
        self.notify_changes.emit()

    def update_view(self) -> Tuple[dict, dict]:
        list_of_files = self.base_dir.files
        list_of_dirs = self.base_dir.dirs
        return list_of_files, list_of_dirs
