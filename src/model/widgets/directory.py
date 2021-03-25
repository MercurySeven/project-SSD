import os

from src.model.network.node import Type
from src.model.network.tree_node import TreeNode
from src.model.widgets.file import File


class Directory:

    def __init__(self, tree: TreeNode, override_name: str = None):
        self._name = tree.get_name() if override_name is None else override_name
        self._path = tree.get_payload().path
        self._files = []
        self._dirs = []
        self._creation_date = tree.get_payload().created_at
        self._last_modified_date = tree.get_updated_at()
        self._node = tree
        self.update_list_of_content()

    def update_list_of_content(self) -> None:
        self._files.clear()
        self._dirs.clear()
        if not self._path or not os.path.isdir(self._path):
            return
        content = self._node.get_children()
        for entry in content:
            if entry.get_payload().type == Type.File:
                self._files.append(File(entry))
            else:
                self._dirs.append(Directory(entry))

    def get_name(self) -> str:
        return self._name

    def get_creation_date(self):
        return self._creation_date

    def get_last_modified_date(self):
        return self._last_modified_date

    def get_path(self) -> str:
        return self._path

    def set_path(self, path) -> None:
        self._path = path

    def set_name(self, name) -> None:
        self._name = name

    @property
    def dirs(self):
        return self._dirs

    @property
    def files(self):
        return self._files

    @property
    def node(self):
        return self._node
