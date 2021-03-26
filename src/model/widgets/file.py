import os
from datetime import datetime
from src.model.network.tree_node import TreeNode
from .settings_model import SettingsModel


class File:
    def __init__(self, node: TreeNode):
        self._name = node.get_name()
        self._creation_date = self._convert_int_to_date(node.get_payload().created_at)
        self._last_modified_date = self._convert_int_to_date(node.get_updated_at())
        self._file_type = node.get_payload().type
        self._size = SettingsModel.convert_size(os.stat(node.get_payload().path).st_size)
        self._status = 'status'
        self._path = node.get_payload().path

    def get_name(self) -> str:
        return self._name

    def get_creation_date(self) -> str:
        return self._creation_date

    def get_last_modified_date(self) -> str:
        return self._last_modified_date

    def get_type(self) -> str:
        return self._file_type

    def get_size(self) -> str:
        return self._size

    def get_status(self) -> str:
        return self._status

    def get_path(self) -> str:
        return self._path

    @staticmethod
    def _convert_int_to_date(time: int) -> str:
        return datetime.fromtimestamp(time).strftime("%H:%M:%S %d/%m/%Y")
