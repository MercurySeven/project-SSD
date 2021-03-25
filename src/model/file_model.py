import os
from typing import Tuple

from PySide6.QtCore import (QSettings, Signal, Slot, QObject)

from src.algorithm import tree_builder
from src.model.widgets.directory import Directory


class FileModel(QObject):
    Sg_model_changed = Signal()

    def __init__(self):
        super(FileModel, self).__init__()
        self.settings = QSettings()
        self.tree = tree_builder.get_tree_from_system(self.settings.value("sync_path"))
        self.base_dir = Directory(self.tree)
        self._current_node = self.tree
        self._current_dir = self.base_dir
        self._current_parent = self.tree._parent

    # per ora ritorna solamente il contenuto del primo livello della directory
    # TODO ampliare la ricerca di una cartella e di un file

    @Slot()
    def Sl_update_model(self) -> None:
        self.tree = tree_builder.get_tree_from_system(self._current_node.get_payload().path)
        self.base_dir._node = self.tree
        self.base_dir.update_list_of_content()
        self.Sg_model_changed.emit()

    def get_data(self) -> Tuple[dict, dict]:
        list_of_files = self.base_dir.files
        list_of_dirs = self.base_dir.dirs
        if self._current_node.get_payload().path != self.base_dir.get_path():
            self._current_dir = Directory(self._current_parent, '...')
            list_of_dirs.insert(0, self._current_dir)
        return list_of_files, list_of_dirs

    def set_current_node(self, path):
        self._current_parent = self._current_node
        if (self._current_node._payload.path != self.base_dir.get_path()):
            if (self._current_node._parent.get_payload().path == path):
                self._current_node = self._current_node._parent
            else:
                self._current_node = self._current_node.get_child_from_path(path)
        else:
            self._current_node = self._current_node.get_child_from_path(path)
        # if self._current_node is None
        #  self._current_node = self.search_node_from_path(path)
        self._current_parent = self._current_node._parent
        self.base_dir._node = self._current_node
        self.Sl_update_model()

    def search_node_from_path(self, path: str):
        relative_path = path
        relative_path = relative_path[relative_path.find(self.base_dir.get_name()):]
        folders = relative_path.split('/')
        folders = folders[1:]
        if os.path.isdir(self.settings.value("sync_path")) is not True:
            return None
        prev_node = self.base_dir.node
        for f in folders:
            folder_found = self._search_through_children(f)
            if folder_found is not None:
                prev_node = folder_found
            else:
                return prev_node
        return prev_node

    def _search_through_children(self, name):
        children = self.tree.get_children()
        for i in children:
            if i.get_payload().name == name:
                return i
        return None
