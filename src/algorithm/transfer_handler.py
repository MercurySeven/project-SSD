from src.model.network.tree_node import TreeNode
import os
import src.network.api as api


def download_folder(node: TreeNode, path: str) -> None:
    """Il nodo rappresenta la cartella che non esiste"""
    path_folder = os.path.join(path, node.get_name())
    os.mkdir(path_folder)
    for _node in node._children:
        if _node.is_directory():
            download_folder(_node, path_folder)
        else:
            download_file(_node, path_folder)


def upload_folder(node: TreeNode, parent_folder_id: str = "LOCAL_ROOT") -> None:
    """Il nodo rappresenta la cartella che non esiste nel server"""
    parent_folder_id = api.create_folder(node.get_name(), parent_folder_id)

    for _node in node._children:
        if _node.is_directory():
            upload_folder(_node, parent_folder_id)
        else:
            upload_file(_node, parent_folder_id)


def download_file(node: TreeNode, path_folder: str) -> None:
    api.download_node_from_server(node, path_folder)


def upload_file(node: TreeNode, parent_folder_id: str) -> None:
    api.upload_node_to_server(node, parent_folder_id)


def delete_node(node_id: str) -> None:
    api.delete_node(node_id)
