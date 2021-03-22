from .tree_node import TreeNode
from network.api import API
from src import settings
import os

api = API(settings.get_username(), settings.get_password())


def download_folder(node: TreeNode, path: str) -> None:
    for _node in node._children:
        if not _node.is_directory():
            api.download_node_from_server(_node, path)
        else:
            path_folder = os.path.join(path, _node.get_name())
            os.mkdir(path_folder)
            download_folder(_node, path_folder)


def upload_folder(node: TreeNode, parent_folder_id: str = "LOCAL_ROOT") -> None:
    parent_folder_id = api.create_folder(node.get_name(), parent_folder_id)

    for _node in node._children:
        if not _node.is_directory():
            api.upload_node_to_server(_node, parent_folder_id)
        else:
            # Crea cartella da network, poi con l'id chiamo ricorsione
            folder_id = api.create_folder(_node.get_name(), parent_folder_id)
            upload_folder(_node, folder_id)
