import os
import pathlib
import sys
import unittest
import platform

from PySide6.QtCore import QSettings, QCoreApplication
import requests.exceptions

from src import settings
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import Status
from src.network.api_exceptions import APIException
from src.network.api_implementation import ExceptionsHandler

node_name = "CLIENT_NODE"


class DefaultCode(unittest.TestCase):
    BLACKLISTED_OS_FOR_CI = "Linux-5.4.0-1046-azure-x86_64-with-glibc2.31"
    app = None
    if platform.platform() != BLACKLISTED_OS_FOR_CI:
        from PySide6.QtWidgets import QApplication
        app = QApplication(sys.argv)
    ORGANIZATION_NAME = "MercurySeven"
    APPLICATION_NAME = "SSD"
    SYNC_ENV_VARIABLE = "sync_path"
    USERNAME_ENV_VARIABLE = "Credentials/user"
    PWD_ENV_VARIABLE = "Credentials/password"
    CONFIG_FILE_NAME = "config.ini"

    def setUp(self) -> None:
        QCoreApplication.setOrganizationName(self.ORGANIZATION_NAME)
        QCoreApplication.setApplicationName(self.APPLICATION_NAME)
        self.env_settings = QSettings()
        self.restore_path = self.env_settings.value(self.SYNC_ENV_VARIABLE)
        self.restore_credentials = [self.env_settings.value(
            self.USERNAME_ENV_VARIABLE), self.env_settings.value(self.PWD_ENV_VARIABLE)]

        path = os.path.join(str(pathlib.Path().absolute()), "tests")
        path = r'%s' % path
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        self.env_settings.setValue(self.SYNC_ENV_VARIABLE, path)
        settings.file_name = os.path.join(path, self.CONFIG_FILE_NAME)
        settings.check_file()

        # return [restore_path, env_settings, restore_credentials]

    def get_env_settings(self):
        return self.env_settings

    def tearDown(self) -> None:
        if os.path.exists(settings.file_name):
            try:
                os.remove(settings.file_name)
            except Exception as e:
                print(e)
        self.env_settings.setValue("sync_path", self.restore_path)
        self.env_settings.setValue("Credentials/user", self.restore_credentials[0])
        self.env_settings.setValue("Credentials/password", self.restore_credentials[1])
        del self.env_settings
        del self.restore_path
        del self.restore_credentials


def _get_test_node(name: str = "test", path: str = "test",
                   updated: int = 200, created: int = 100):
    return TreeNode(Node(node_name, name,
                         Type.Folder, created, updated, path))


def _get_file_test_node(name: str = "test", path: str = "test",
                        updated: int = 200, created: int = 100):
    return TreeNode(Node(node_name, name,
                         Type.File, created, updated, path))


def create_folder_with_folders(folder_list: list = None, time: int = 100):
    root_folder = _get_test_node()
    if folder_list is None:
        folder_list = []
    for el in folder_list:
        root_folder.add_node(_get_test_node(el, el, time, time))
    return root_folder


def create_folder_with_files(file_list: list = None, time: int = 100):
    root_folder = _get_test_node()
    if file_list is None:
        file_list = []
    for el in file_list:
        root_folder.add_node(_get_file_test_node(el, el, time, time))
    return root_folder


def _get_default_dict(upd: int = 2000) -> dict:
    _id = "id"
    _name = "name"
    _type = "File"
    _created = 2000
    _updated = upd
    _size = 14
    _email = "a@a.it"
    thisdict = {
        "id": _id,
        "name": _name,
        "type": _type,
        "created_at": _created,
        "updated_at": _updated,
        "size": _size,
        "last_editor": {
            "email": _email
        }
    }
    return thisdict


def _get_tree_dict() -> dict:
    _id = "id"
    _name = "name"
    _type = "Folder"
    _created = 2000
    _updated = 2000
    _size = 14
    thisdict = {
        "getNode": {
            "id": _id,
            "name": _name,
            "type": _type,
            "created_at": _created,
            "updated_at": _updated,
            "size": _size,
            "last_editor": None,
            "children": [_get_default_dict()]
        }
    }
    return thisdict


def _get_special_tree_dict() -> dict:
    _id = "id"
    _name = "name.ciao.we"
    _type = "Folder"
    _created = 1
    _updated = 1
    thisdict = {
        "getNode": {
            "id": _id,
            "name": _name,
            "type": _type,
            "created_at": _created,
            "updated_at": _updated,
            "last_editor": None,
            "children": [_get_default_dict(_updated)]
        }
    }
    return thisdict


class ResultObj:
    def __init__(self, action, _lun: int = 0, _name: str = "test", snap_upd: int = 1):
        self.result = {
            "action": action,
            "node": _get_test_node(_name),
            "path": "test",
            "id": "id",
            "snap_last_update": snap_upd
        }
        self.lun = _lun
        self.id = {
            "getNode": {
                "size": 100
            }
        }
        self.name = _name

    def get_updated_at(self):
        return 1

    # metodo usato per poter usare len(obj)
    def __len__(self):
        return self.lun

    # metodo usato per poter iterare sull'oggetto
    def __iter__(self):
        yield self.result

    def quit(self):
        pass

    def show(self):
        pass

    def get_name(self):
        return self.name


class FakeLogger:
    def info(self, text: str):
        pass


class NodeMetadata:

    def __init__(self, updated_at: int = 1000):
        self.updated = updated_at

    def get_content_from_node(self):
        return {'getNode': {'updated_at': self.updated}, 'random': {'random': 2}}


class RequestObj:
    def __init__(self, _text: str = "test", _status: Status = Status.Ok):
        self.text = _text
        self.status_code = _status
        self.ok = _status if _status == Status.Ok else None
        self.content = b"test"

    def set_text(self, _text):
        self.text = _text

    def json(self):
        return {'user_info': {'id': 1}, 'auth_token': {'cookie': 2}}

    @ExceptionsHandler
    def function_network_exception(self):
        raise requests.exceptions.ConnectionError("test")

    @ExceptionsHandler
    def function_server_exception(self):
        raise requests.exceptions.HTTPError("test")

    def raise_for_status(self):
        if self.status_code == Status.Error:
            raise APIException()
