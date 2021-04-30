from datetime import datetime

from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.file import File


class RemoteFile(File):
    def __init__(self, node: TreeNode):
        super().__init__(node)
        self._status = 'status'
        self.id = node.get_payload().id

    def get_status(self) -> str:
        return self._status

    @staticmethod
    def _convert_int_to_date(time: int) -> str:
        return datetime.fromtimestamp(time).strftime("%H:%M:%S %d/%m/%Y")
