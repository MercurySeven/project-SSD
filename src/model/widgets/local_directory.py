from src.model.widgets.directory import Directory

import os

from src.model.algorithm.node import Type
from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.file import File


class LocalDirectory(Directory):
    def __init__(self, tree: TreeNode, override_name: str = None):
        super(LocalDirectory, self).__init__(tree, override_name)
        self._path = tree.get_payload().path
        self._dirs = []
        self.update_list_of_content()

    def update_list_of_content(self) -> None:
        self._files.clear()
        self._dirs.clear()
        if self._path is None or not os.path.isdir(self._path):
            return
        content = self._node.get_children()
        for entry in content:
            if entry.get_payload().type == Type.File:
                self._files.append(File(entry))
            else:
                self._dirs.append(LocalDirectory(entry))

    def get_path(self) -> str:
        return self._path
