from PySide6.QtCore import (QObject, Signal)

from src import settings
from src.network import api
from src.network.cookie_session import BadResponse


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

    def get_all_files(self, node_id: str = "LOCAL_ROOT") -> list:
        return api.get_all_files(node_id)

    def upload_to_server(self, file_path: str) -> None:
        return api.upload_to_server(file_path)

    def download_from_server(self, file_path: str,
                             file_name: str,
                             file_id: str,
                             created_at: int,
                             updated_at: int
                             ) -> None:
        api.download_from_server(file_path, file_name, file_id, created_at, updated_at)

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
