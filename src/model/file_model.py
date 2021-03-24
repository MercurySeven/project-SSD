from typing import Tuple

from PySide6.QtCore import (QSettings, Signal, Slot, QObject)

from src.model.widgets.directory import Directory
from src.model.network import tree_builder as root


class FileModel(QObject):
    Sg_model_changed = Signal()

    def __init__(self):
        super(FileModel, self).__init__()
        self.settings = QSettings()
        self.tree = root.get_tree_from_system(self.settings.value("sync_path"))
        self.base_dir = Directory(str(self.settings.value("sync_path")).split(
            '/')[-1], self.settings.value("sync_path"), "adesso", self.tree)
        self._current_node = self.tree

    # per ora ritorna solamente il contenuto del primo livello della directory
    # TODO ampliare la ricerca di una cartella e di un file

    @Slot()
    def Sl_update_model(self) -> None:
        self.base_dir.update_list_of_content()
        self.Sg_model_changed.emit()

    def get_data(self) -> Tuple[dict, dict]:
        list_of_files = self.base_dir.files
        list_of_dirs = self.base_dir.dirs
        return list_of_files, list_of_dirs

    def set_current_node(self, path):
        self._current_node = self._current_node.get_child_from_path(path)
        self.base_dir = Directory(self._current_node.get_payload().name,
                                  self.settings.value("sync_path"), "adesso", self._current_node)
        self.Sl_update_model()
