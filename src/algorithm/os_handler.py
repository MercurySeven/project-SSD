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
            path_folder = os.path.join(path, _node._name)
            os.mkdir(path_folder)
            created_at = _node._payload.created_at
            updated_at = _node._payload.updated_at
            os.utime(path_folder, (created_at, updated_at))
            download_folder(_node, path_folder)
