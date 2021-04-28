from abc import ABC, abstractmethod

from src.model.algorithm.tree_node import TreeNode


class Api(ABC):
    @abstractmethod
    def login(self, username: str, password: str):
        pass

    @abstractmethod
    def is_logged(self) -> bool:
        pass

    @abstractmethod
    def get_info_from_email(self):
        pass

    @abstractmethod
    def get_user_id(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def upload_node(self):
        pass

    @abstractmethod
    def download_node(self, node: TreeNode, path: str, quota_libera: int):
        pass

    @abstractmethod
    def delete_node(self):
        pass

    @abstractmethod
    def get_content_from_node(self):
        pass

    @abstractmethod
    def create_folder(self):
        pass
