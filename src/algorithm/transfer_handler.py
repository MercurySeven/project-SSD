import os
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel


networkmodel: NetworkModel = None


def set_model(model: NetworkModel):
    global networkmodel
    networkmodel = model


def download_folder(node: TreeNode, path: str) -> None:
    """Il nodo rappresenta la cartella che non esiste"""
    path_folder = os.path.join(path, node.get_name())
    os.mkdir(path_folder)
    for _node in node.get_children():
        if _node.is_directory():
            download_folder(_node, path_folder)
        else:
            download_file(_node, path_folder)


def upload_folder(node: TreeNode, parent_folder_id: str = "LOCAL_ROOT") -> None:
    """Il nodo rappresenta la cartella che non esiste nel server"""
    global networkmodel

    parent_folder_id = networkmodel.create_folder(node.get_name(), parent_folder_id)

    for _node in node.get_children():
        if _node.is_directory():
            upload_folder(_node, parent_folder_id)
        else:
            upload_file(_node, parent_folder_id)


def download_file(node: TreeNode, path_folder: str) -> None:
    global networkmodel
    networkmodel.download_file(node, path_folder)


def upload_file(node: TreeNode, parent_folder_id: str) -> None:
    networkmodel
    networkmodel.upload_file(node, parent_folder_id)


def delete_node(node_id: str) -> None:
    networkmodel
    networkmodel.delete_node(node_id)
