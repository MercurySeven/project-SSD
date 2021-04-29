import os
from typing import Tuple, Optional

from PySide6.QtCore import (QSettings, Signal, Slot, QObject)

from src.algorithm import tree_builder
from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.local_directory import LocalDirectory
from src.model.widgets.file import File


class FileModel(QObject):
    Sg_model_changed = Signal()
    __model = None

    __create_key = object()

    @classmethod
    def get_instance(cls):
        if FileModel.__model is None:
            FileModel.__model = FileModel(cls.__create_key)
        return FileModel.__model

    def __init__(self, create_key):
        assert (create_key == FileModel.__create_key), \
            "FileModel objects must be created using NetworkModel.create"

        super(FileModel, self).__init__()
        self.settings = QSettings()
        self.tree = tree_builder.get_tree_from_system(self.settings.value("sync_path"))
        self.current_folder = LocalDirectory(self.tree, self.tree.get_name())
        self.previous_folder = None

    @Slot()
    def Sl_update_model(self) -> None:
        # ricreo tree dalla root
        self.tree = tree_builder.get_tree_from_system(self.settings.value("sync_path"))
        self.current_folder._node = self.search_node_from_path(
            self.current_folder._node.get_payload().path)  # cerco il nodo attuale nel nuovo tree
        self.current_folder.update_list_of_content()  # aggiorno lista carelle e file
        self.Sg_model_changed.emit()

    def get_data(self) -> Tuple[list[File], list[LocalDirectory]]:
        list_of_files = self.current_folder._files  # lista file dalla dir
        list_of_dirs = self.current_folder._dirs  # lista dir dalla dir

        if self.current_folder._node._parent:
            self.previous_folder = LocalDirectory(self.current_folder._node._parent, '..')
            list_of_dirs.insert(0, self.previous_folder)

        return list_of_files, list_of_dirs

    def set_current_node(self, path) -> None:
        name = path.split('/')[-1]  # ottengo nome folder desiderato
        child = self._search_through_children(name, self.current_folder._node)  # cerco figlio
        if(child):
            # imposto figlio come node folder
            self.current_folder._node = child
        else:
            # imposto genitore come node folder
            self.current_folder._node = self.search_node_from_path(path)
        self.Sl_update_model()

    def search_node_from_path(self, path: str) -> Optional[TreeNode]:
        relative_path = path
        folder_name = self.settings.value("sync_path").split(os.sep)[-1]
        relative_path = relative_path[relative_path.find(folder_name):]
        folders = relative_path.split(os.path.sep)
        curr_node = self.tree
        if self.tree.get_payload().name == "ROOT":
            folders = folders[1:]
            for f in folders:
                folder_found = self._search_through_children(f, curr_node)
                if folder_found is None:
                    return curr_node
                else:
                    curr_node = folder_found
            return curr_node
        else:
            return None

    def _search_through_children(self, name, node) -> Optional[TreeNode]:
        children = node.get_children()
        for i in children:
            if i.get_payload().name == name:
                return i
        return None
