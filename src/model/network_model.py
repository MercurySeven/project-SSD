from PySide6.QtCore import (QObject, Signal, QSettings)
from src.network import api
from src.network.api_exceptions import (APIException, LoginError, NetworkError, ServerError)
from src.model.algorithm.tree_node import TreeNode
from functools import wraps
import logging


def RetryLogin(func):
    """se si verificano ServerError è possibile che il login sia scaduto
    quindi tento di rifare il login e riprovare a chiamare la funzione
    nella speranza che funzioni"""

    logger = logging.getLogger("NetworkModel.RetryLogin")

    @wraps(func)
    def handle(self, *args, **kwargs):
        try:

            logger.debug(f"call {func.__name__}...")
            return func(self, *args, **kwargs)

        except ServerError as e:
            logger.debug(f"{func.__name__} exit with error: {str(e)}")
            # e' possibile che sia scaduto il login provo a rifarlo
            # e ritento la chiamata
            logger.debug(f"retry {func.__name__} with new login")
            api.login()
            return func(self, *args, **kwargs)

    return handle


def APIExceptionsHandler(func):
    """questa funzione si occupa di gestire le eccezioni alzate dal modulo API
    se un metodo arriva qui allora l'unica cosa che rimane da fare
    e' emettere i segnali per avvisare dell'errore"""

    logger = logging.getLogger("NetworkModel.APIExceptionsHandler")

    @wraps(func)
    def APIExceptionHandle(self, *args, **kwargs):
        try:

            return func(self, *args, **kwargs)

        except APIException as e:
            logger.error(f"{func.__name__} failed")
            logger.error(f"with error {str(e)}")

            if type(e) is LoginError:
                logger.error("Signal Sg_login_failed emitted")
                self.Sg_login_failed.emit()

            elif type(e) is ServerError:
                logger.error("Signal Sg_server_failed emitted")
                self.Sg_server_failed.emit()

            elif type(e) is NetworkError:
                logger.error("Signal Sg_connection_failed emitted")
                self.Sg_server_failed.emit()

    return APIExceptionHandle


class NetworkModel(QObject):
    logger = logging.getLogger("NetworkModel")

    Sg_model_changed = Signal()
    Sg_logout = Signal()

    # error signals
    Sg_login_failed = Signal()
    Sg_connection_failed = Signal()
    Sg_server_failed = Signal()

    def __init__(self):
        super(NetworkModel, self).__init__(None)

        self.env_settings = QSettings()

    @APIExceptionsHandler
    def login(self, user: str = "", password: str = "") -> None:

        NetworkModel.logger.info("try to login...")

        user = user if user else self.env_settings.value("Credentials/user")
        password = password if password else self.env_settings.value("Credentials/password")

        api.login(user, password)
        NetworkModel.logger.info("login successful")

        # save to Qsettings
        NetworkModel.logger.info("saving credentials")
        self.env_settings.setValue("Credentials/user", user)
        self.env_settings.setValue("Credentials/password", password)
        self.env_settings.sync()

        self.Sg_model_changed.emit()

    @APIExceptionsHandler
    @RetryLogin
    def get_info_from_email(self) -> dict[str, str]:
        return api.get_info_from_email()

    @APIExceptionsHandler
    @RetryLogin
    def get_user_id(self) -> str:
        return api.get_user_id()

    @APIExceptionsHandler
    @RetryLogin
    def is_logged(self) -> bool:
        return api.is_logged()

    def get_credentials(self) -> [str, str]:
        return [self.get_username(), self.get_password()]

    def get_username(self) -> str:
        user = self.env_settings.value("Credentials/user")
        return user if user else ""

    def get_password(self) -> str:
        password = self.env_settings.value("Credentials/password")
        return password if password else ""

    @APIExceptionsHandler
    @RetryLogin
    def logout(self) -> bool:
        if api.logout():
            self.message = ""
            return True
        return False

    @APIExceptionsHandler
    @RetryLogin
    def download_file(self, node: TreeNode, path_folder: str) -> None:
        api.download_node_from_server(node, path_folder)

    @APIExceptionsHandler
    @RetryLogin
    def upload_file(self, node: TreeNode, parent_folder_id: str) -> None:
        api.upload_node_to_server(node, parent_folder_id)

    @APIExceptionsHandler
    @RetryLogin
    def delete_node(self, node_id: str) -> None:
        api.delete_node(node_id)

    @APIExceptionsHandler
    @RetryLogin
    def get_content_from_node(self, node_id: str = "LOCAL_ROOT") -> str:
        return api.get_content_from_node(node_id)

    @APIExceptionsHandler
    @RetryLogin
    def create_folder(self, folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
        return api.create_folder(folder_name, parent_folder_id)
