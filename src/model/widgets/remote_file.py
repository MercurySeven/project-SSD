from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.file import File
from src.model.settings_model import SettingsModel


class RemoteFile(File):
    def __init__(self, node: TreeNode):
        super().__init__(node)
        self.id = node.get_payload().id
        self.size = SettingsModel.convert_size(node.get_payload().size)
        self.last_editor = node.get_payload().last_editor
        self._status = 'status'

    def get_status(self) -> str:
        return self._status

    def get_size(self) -> str:
        return self.size

    def get_last_editor(self) -> str:
        return self.last_editor
