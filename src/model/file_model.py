from typing import Tuple

from PySide6.QtCore import (QSettings, Signal, Slot, QObject)

from src.model.widgets.directory import Directory


class FileModel(QObject):
    Sg_model_changed = Signal()

    def __init__(self):
        super(FileModel, self).__init__()
        self.settings = QSettings()
        self.base_dir = Directory(str(self.settings.value("sync_path")).split(
            '/')[-1], self.settings.value("sync_path"), "adesso")
    # per ora ritorna solamente il contenuto del primo livello della directory
    # TODO ampliare la ricerca di una cartella e di un file

    @Slot()
    def Sl_update_model(self) -> None:
        self.base_dir.update_list_of_content()
        self.Sg_model_changed.emit()

    def get_data(self) -> Tuple[dict, dict]:
        list_of_files = self.base_dir._files
        list_of_dirs = self.base_dir._dirs
        return list_of_files, list_of_dirs
