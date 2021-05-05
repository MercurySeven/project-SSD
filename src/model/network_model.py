import logging
from enum import Enum
from functools import wraps
from threading import Lock

from PySide6.QtCore import (QObject, Signal, QSettings)

from src.model.algorithm.tree_node import TreeNode
from src.network.api import Api
from src.network.api_exceptions import (APIException, LoginError, NetworkError, ServerError)
from src.network.api_implementation import ApiImplementation


class Status(Enum):
    Error = "last func ended with error"
    Ok = "last func ended normally"


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
            api_impl = ApiImplementation()
            api_impl.login()
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

            ret = func(self, *args, **kwargs)
            self.status = Status.Ok
            return ret

        except APIException as e:
            logger.error(f"{func.__name__} failed")
            logger.error(f"with error {str(e)}")

            # update status
            self.status = Status.Error

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


class NetworkMeta(type(QObject), type(Api)):
    pass


class NetworkModel(QObject, Api, metaclass=NetworkMeta):
    logger = logging.getLogger("NetworkModel")
    __model = None

    status: Status = Status.Ok

    Sg_model_changed = Signal()
    Sg_logout = Signal()

    # error signals
    Sg_login_failed = Signal()
    Sg_connection_failed = Signal()
    Sg_server_failed = Signal()

    __create_key = object()

    @classmethod
    def get_instance(cls):
        if NetworkModel.__model is None:
            NetworkModel.__model = NetworkModel(cls.__create_key)
        return NetworkModel.__model

    def __init__(self, create_key):

        assert (create_key == NetworkModel.__create_key), \
            "NetworkModel objects must be created using NetworkModel.get_instance()"
        super(NetworkModel, self).__init__(None)
        super(Api, self).__init__()

        self.api_implementation = ApiImplementation()
        self.env_settings = QSettings()
        self.lock = Lock()

    def raise_for_status(self):
        if self.status == Status.Error:
            raise APIException()

    @APIExceptionsHandler
    def login(self, user: str = "", password: str = "") -> None:

        NetworkModel.logger.info("try to login...")

        user = user if user else self.env_settings.value("Credentials/user")
        password = password if password else self.env_settings.value("Credentials/password")

        self.api_implementation.login(user, password)
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
        self.lock.acquire()
        try:
            return self.api_implementation.get_info_from_email()
        finally:
            self.lock.release()

    @APIExceptionsHandler
    @RetryLogin
    def get_user_id(self) -> str:
        self.lock.acquire()
        try:
            return self.api_implementation.get_user_id()
        finally:
            self.lock.release()

    @APIExceptionsHandler
    @RetryLogin
    def is_logged(self) -> bool:
        return self.api_implementation.is_logged()

    def get_username(self) -> str:
        user = self.env_settings.value("Credentials/user")
        return user if user else ""

    def get_password(self) -> str:
        password = self.env_settings.value("Credentials/password")
        return password if password else ""

    @APIExceptionsHandler
    @RetryLogin
    def logout(self) -> bool:
        self.lock.acquire()
        try:
            if self.api_implementation.logout():
                self.message = ""
                self.env_settings.setValue("Credentials/user", None)
                self.env_settings.setValue("Credentials/password", None)
                return True
            return False
        finally:
            self.lock.release()

    @RetryLogin
    def download_node(self, node: TreeNode, path_folder: str, quota_libera: float) -> dict:
        remote_node = self.api_implementation.get_content_from_node(node.get_payload().id)
        file_size = remote_node["getNode"]["size"]

        # Se ho spazio procedo al download
        if quota_libera > file_size:
            result = self.api_implementation.download_node(node, path_folder)
            return {
                "node_name": node.get_name(),
                "result": result,
                "type": "network_error" if not result else ""
            }

        return {
            "node_name": node.get_name(),
            "result": False,
            "type": "space_error"
        }

    @RetryLogin
    def upload_node(self, node: TreeNode, parent_folder_id: str) -> None:
        self.api_implementation.upload_node(node, parent_folder_id)

    @RetryLogin
    def delete_node(self, node_id: str) -> None:
        self.lock.acquire()
        try:
            self.api_implementation.delete_node(node_id)
        finally:
            self.lock.release()

    @RetryLogin
    def get_content_from_node(self, node_id: str = "LOCAL_ROOT") -> str:
        self.lock.acquire()
        try:
            return self.api_implementation.get_content_from_node(node_id)
        finally:
            self.lock.release()

    @RetryLogin
    def create_folder(self, folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
        self.lock.acquire()
        try:
            return self.api_implementation.create_folder(folder_name, parent_folder_id)
        finally:
            self.lock.release()
