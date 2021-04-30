from datetime import datetime

from src.model.algorithm.tree_node import TreeNode


class File:
    def __init__(self, node: TreeNode):
        self._name = node.get_name()
        self._creation_date = self._convert_int_to_date(node.get_payload().created_at)
        self._last_modified_date = self._convert_int_to_date(node.get_updated_at())

    def get_name(self) -> str:
        return self._name

    def get_creation_date(self) -> str:
        return self._creation_date

    def get_last_modified_date(self) -> str:
        return self._last_modified_date

    @staticmethod
    def _convert_int_to_date(time: int) -> str:
        return datetime.fromtimestamp(time).strftime("%H:%M:%S %d/%m/%Y")
