from typing import Tuple, Optional

from PySide6.QtCore import (Signal, Slot, QObject)

from src.algorithm import tree_builder
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel
from src.model.widgets.remote_directory import RemoteDirectory
from src.model.widgets.file import File
from src.model.algorithm.node import Type


class RemoteFileModel(QObject):
    Sg_model_changed = Signal()
    __model = None

    __create_key = object()

    @classmethod
    def get_instance(cls, network_model: NetworkModel):
        if RemoteFileModel.__model is None:
            RemoteFileModel.__model = RemoteFileModel(network_model, cls.__create_key)
        return RemoteFileModel.__model

    def __init__(self, network_model: NetworkModel, create_key):
        assert (create_key == RemoteFileModel.__create_key), \
            "RemoteFileModel objects must be created using NetworkModel.create"

        super(RemoteFileModel, self).__init__()
        tree_builder.set_model(network_model)
        self.folder_queue = ["LOCAL_ROOT"]

        self.tree = tree_builder.get_tree_children_from_node_id("LOCAL_ROOT")
        # self.search_node_from_id(self.tree.get_payload().id)

    @Slot()
    def Sl_update_model(self) -> None:
        # ricreo tree dalla root
        self.tree = tree_builder.get_tree_from_node_id()

        self.Sg_model_changed.emit()

    def get_current_tree(self):
        self.tree = tree_builder.get_tree_children_from_node_id(self.folder_queue[-1])

    def get_data(self) -> Tuple[list[File], list[RemoteDirectory]]:
        list_of_files = []
        list_of_dirs = []

        content = self.tree
        for entry in content:
            if entry.get_payload().type == Type.File:
                list_of_files.append(File(entry))
            else:
                list_of_dirs.append(RemoteDirectory(entry))

        if self.folder_queue[-1] != "LOCAL_ROOT":
            self.previous_folder = RemoteDirectory(self.current_folder._node._parent, '..')
            list_of_dirs.insert(0, self.previous_folder)

        return list_of_files, list_of_dirs

    ''' def set_current_node(self, path) -> None:
        name = path.split('/')[-1]  # ottengo nome folder desiderato
        child = self._search_through_children(name, self.current_folder._node)  # cerco figlio
        if(child):
            # imposto figlio come node folder
            self.current_folder._node = child
        else:
            # imposto genitore come node folder
            self.current_folder._node = self.search_node_from_path(path)
        self.Sl_update_model() '''

    '''def search_node_from_id(self, id: str) -> Optional[TreeNode]:
        n = self.tree.get_children()
        for i in n:
            print(i.get_name())

    def _search_through_children(self, id, node) -> Optional[TreeNode]:
        children = node.get_children()
        for i in children:
            if i.get_payload().id == id:
                return i
        return None'''
