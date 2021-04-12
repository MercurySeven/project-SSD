import os
import pathlib
import sys

from PySide6.QtCore import QSettings, QCoreApplication
from PySide6.QtWidgets import QApplication

from src import settings
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode

node_name = "CLIENT_NODE"
app = QApplication(sys.argv)


def setUp() -> [str, QSettings]:
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")
    env_settings = QSettings()
    restore_path = env_settings.value("sync_path")

    path = os.path.join(str(pathlib.Path().absolute()), "tests")
    path = r'%s' % path
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    env_settings.setValue("sync_path", path)
    settings.file_name = os.path.join(path, "config.ini")
    settings.check_file()

    return [restore_path, env_settings]


def tearDown(env_settings: QSettings, restore_path) -> None:
    if os.path.exists(settings.file_name):
        try:
            os.remove(settings.file_name)
        except Exception as e:
            print(e)
    env_settings.setValue("sync_path", restore_path)


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
