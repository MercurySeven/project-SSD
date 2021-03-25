from src.model.network.tree_node import TreeNode
import os
from .settings_model import SettingsModel


class File:
    def __init__(self, node: TreeNode):
        self._name = node.get_name()
        self._creation_date = node.get_payload().created_at
        self._last_modified_date = node.get_updated_at()
        self._file_type = node.get_payload().type
        self._size = SettingsModel.convert_size(os.stat(node.get_payload().path).st_size)
        self._status = 'status'

    def get_name(self) -> str:
        return self._name

    def get_creation_date(self) -> str:
        return self._creation_date

    def get_last_modified_date(self) -> str:
        return self._last_modified_date

    def get_type(self) -> str:
        return self._file_type

    def get_size(self) -> str:
        return str(self._size)

    def get_status(self) -> str:
        return self._status

    def set_name(self, name: str) -> None:
        self._name = name

    def set_creation_date(self, creation_date: str) -> None:
        self._creation_date = creation_date

    def set_last_modified_date(self, last_modified_date: str) -> None:
        self._last_modified_date = last_modified_date

    def set_type(self, _file_type: str) -> None:
        self._file_type = _file_type

    def set_size(self, size: int) -> None:
        self._size = self._right_size(size)

    def set_status(self, status: str) -> None:
        self._status = status
