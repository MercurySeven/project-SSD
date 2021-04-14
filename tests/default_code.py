import os
import pathlib

from PySide6.QtCore import QSettings, QCoreApplication
import requests.exceptions
from src import settings
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import Status
from src.network.api_exceptions import APIException
from src.network.api_implementation import ExceptionsHandler

node_name = "CLIENT_NODE"


def setUp() -> [str, QSettings]:
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")
    env_settings = QSettings()
    restore_path = env_settings.value("sync_path")
    restore_credentials = [env_settings.value(
        "Credentials/user"), env_settings.value("Credentials/password")]

    path = os.path.join(str(pathlib.Path().absolute()), "tests")
    path = r'%s' % path
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    env_settings.setValue("sync_path", path)
    settings.file_name = os.path.join(path, "config.ini")
    settings.check_file()

    return [restore_path, env_settings, restore_credentials]


def tearDown(env_settings: QSettings, restore_path: str, restore_credentials: [str, str]) -> None:
    if os.path.exists(settings.file_name):
        try:
            os.remove(settings.file_name)
        except Exception as e:
            print(e)
    env_settings.setValue("sync_path", restore_path)
    env_settings.setValue("Credentials/user", restore_credentials[0])
    env_settings.setValue("Credentials/password", restore_credentials[1])


def _get_test_node():
    updated = 200
    created = 100
    return TreeNode(Node(node_name, "test",
                         Type.Folder, created, updated, "test"))


def _get_default_dict() -> dict:
    _id = "id"
    _name = "name"
    _type = "File"
    _created = 2000
    _updated = 2000
    thisdict = {
        "id": _id,
        "name": _name,
        "type": _type,
        "created_at": _created,
        "updated_at": _updated
    }
    return thisdict


def _get_tree_dict() -> dict:
    _id = "id"
    _name = "name"
    _type = "Folder"
    _created = 2000
    _updated = 2000
    thisdict = {
        "getNode": {
            "id": _id,
            "name": _name,
            "type": _type,
            "created_at": _created,
            "updated_at": _updated,
            "children": [_get_default_dict()]
        }
    }
    return thisdict


class ResultObj:
    def __init__(self, action, _lun: int = 0):
        self.result = {
            "action": action,
            "node": _get_test_node(),
            "path": "test",
            "id": "id"
        }
        self.lun = _lun

    # metodo usato per poter usare len(obj)
    def __len__(self):
        return self.lun

    # metodo usato per poter iterare sull'oggetto
    def __iter__(self):
        yield self.result

    def quit(self):
        pass


class RequestObj:
    def __init__(self, _text: str = "test", _status: Status = Status.Ok):
        self.text = _text
        self.status_code = _status
        self.ok = _status if _status == Status.Ok else None
        self.content = b"test"

    def set_text(self, _text):
        self.text = _text

    @ExceptionsHandler
    def function_network_exception(self):
        raise requests.exceptions.ConnectionError("test")

    @ExceptionsHandler
    def function_server_exception(self):
        raise requests.exceptions.HTTPError("test")

    def raise_for_status(self):
        if self.status_code == Status.Error:
            raise APIException()
