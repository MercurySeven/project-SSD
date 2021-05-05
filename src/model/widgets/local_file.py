import os

from src.model.algorithm.tree_node import TreeNode
from src.model.settings_model import SettingsModel
from src.model.widgets.file import File


class LocalFile(File):
    def __init__(self, node: TreeNode):
        super().__init__(node)
        self._path = node.get_payload().path
        self._size = SettingsModel.convert_size(os.stat(node.get_payload().path).st_size)

    def get_size(self) -> str:
        return self._size

    def get_path(self) -> str:
        return self._path
