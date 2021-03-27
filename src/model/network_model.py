from PySide6.QtCore import (QObject, Signal)

from src import settings
from src.network import api
from src.network.cookie_session import BadResponse
from src.model.algorithm.tree_node import TreeNode


class NetworkModel(QObject):
    Sg_model_changed = Signal()

    def __init__(self):
        super(NetworkModel, self).__init__(None)
        self.message = ""

    def login(self, username, password) -> None:
        try:
            api.login(username, password)
            api.set_username_and_pwd(username, password)
            settings.update_login_credentials(username, password)
            self.message = "Success"
        except (ValueError, BadResponse, ConnectionError) as error:
            self.message = str(error)
        finally:
            self.Sg_model_changed.emit()

    def get_info_from_email(self) -> dict[str, str]:
        return api.get_info_from_email()

    def get_user_id(self) -> str:
        return api.get_user_id()

    def is_logged(self) -> bool:
        return api.is_logged()

    def get_message(self) -> str:
        return self.message

    def get_credentials(self) -> [str, str]:
        return [settings.get_username(), settings.get_password()]

    def get_username(self) -> str:
        return settings.get_username() if settings.get_username() is not None else ""

    def get_password(self) -> str:
        return settings.get_password() if settings.get_password() is not None else ""

    def logout(self) -> bool:
        if api.logout():
            self.message = ""
            return True
        return False

    def download_file(node: TreeNode, path_folder: str) -> None:
        api.download_node_from_server(node, path_folder)

    def upload_file(node: TreeNode, parent_folder_id: str) -> None:
        api.upload_node_to_server(node, parent_folder_id)

    def delete_node(node_id: str) -> None:
        api.delete_node(node_id)
