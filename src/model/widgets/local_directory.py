import os

from src.model.algorithm.node import Type
from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.local_file import LocalFile


class LocalDirectory:
    def __init__(self, tree: TreeNode, override_name: str = None):
        self._name = tree.get_name() if override_name is None else override_name
        self._node = tree
        self._files = []
        self._dirs = []
        self._path = tree.get_payload().path
        self.update_list_of_content()

    def update_list_of_content(self) -> None:
        self._files.clear()
        self._dirs.clear()
        if self._path is None or not os.path.isdir(self._path):
            return
        content = self._node.get_children()
        for entry in content:
            if entry.get_payload().type == Type.File:
                self._files.append(LocalFile(entry))
            else:
                self._dirs.append(LocalDirectory(entry))

    def get_path(self) -> str:
        return self._path

    def get_name(self) -> str:
        return self._name
