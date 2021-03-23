from .tree_node import TreeNode
from network.api import API
from src import settings
import os

api = API(settings.get_username(), settings.get_password())


def download_folder(node: TreeNode, path: str) -> None:
    """Il nodo rappresenta la cartella che non esiste"""
    path_folder = os.path.join(path, node.get_name())
    os.mkdir(path_folder)
    for _node in node._children:
        if _node.is_directory():
            download_folder(_node, path_folder)
        else:
            api.download_node_from_server(_node, path_folder)


def upload_folder(node: TreeNode, parent_folder_id: str = "LOCAL_ROOT") -> None:
    """Il nodo rappresenta la cartella che non esiste nel server"""
    parent_folder_id = api.create_folder(node.get_name(), parent_folder_id)

    for _node in node._children:
        if not _node.is_directory():
            api.upload_node_to_server(_node, parent_folder_id)
        else:
            upload_folder(_node, parent_folder_id)
