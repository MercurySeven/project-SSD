from typing import Tuple

from PySide6.QtCore import (Signal, QObject)

from src.algorithm import tree_builder
from src.model.algorithm.node import Type, Node
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel
from src.model.widgets.remote_directory import RemoteDirectory
from src.model.widgets.remote_file import RemoteFile


class RemoteFileModel(QObject):
    Sg_model_changed = Signal()
    __model = None

    __create_key = object()

    @classmethod
    def get_instance(cls):
        if RemoteFileModel.__model is None:
            RemoteFileModel.__model = RemoteFileModel(cls.__create_key)
        return RemoteFileModel.__model

    def __init__(self, create_key):
        assert (create_key == RemoteFileModel.__create_key), \
            "RemoteFileModel objects must be created using NetworkModel.create"

        super(RemoteFileModel, self).__init__()
        self.folder_queue = ["LOCAL_ROOT"]

    def set_network_model(self, network_model: NetworkModel) -> None:
        tree_builder.set_model(network_model)

    def get_current_tree(self) -> TreeNode:
        return tree_builder.get_tree_from_node_id(self.folder_queue[-1], False)

    def get_data(self) -> Tuple[list[RemoteFile], list[RemoteDirectory]]:
        list_of_files = []
        list_of_dirs = []

        for entry in self.get_current_tree().get_children():
            if entry.get_payload().type == Type.File:
                list_of_files.append(RemoteFile(entry))
            else:
                list_of_dirs.append(RemoteDirectory(entry))

        if self.folder_queue[-1] != "LOCAL_ROOT":
            previous_folder = RemoteDirectory(
                TreeNode(Node(self.folder_queue[-1], '..', Type.Folder, None, None)))
            list_of_dirs.insert(0, previous_folder)

        return list_of_files, list_of_dirs

    def set_current_node(self, id: str) -> None:
        if id in self.folder_queue:
            self.folder_queue.remove(id)
        else:
            self.folder_queue.append(id)
        self.Sg_model_changed.emit()
