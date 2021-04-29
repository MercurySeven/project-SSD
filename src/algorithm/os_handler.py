import os
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel

networkmodel: NetworkModel = None
settingsmodel: SettingsModel = None


def set_model(model: NetworkModel, settings_model: SettingsModel) -> None:
    global networkmodel
    global settingsmodel
    networkmodel = model
    settingsmodel = settings_model


def download_folder(node: TreeNode, path: str) -> list[dict]:
    """Il nodo rappresenta la cartella che non esiste,
    ritorna i risultati dei download che sono stati fatti"""
    path_folder = os.path.join(path, node.get_name())
    os.mkdir(path_folder)

    download_operations_list = []
    for _node in node.get_children():
        if _node.is_directory():
            download_operations_list.extend(download_folder(_node, path_folder))
        else:
            download_operations_list.append(download_file(_node, path_folder))
    return download_operations_list


def upload_folder(node: TreeNode, parent_folder_id: str = "LOCAL_ROOT") -> None:
    """Il nodo rappresenta la cartella che non esiste nel server"""
    parent_folder_id = create_folder(node.get_name(), parent_folder_id)

    for _node in node.get_children():
        if _node.is_directory():
            upload_folder(_node, parent_folder_id)
        else:
            upload_file(_node, parent_folder_id)


def download_file(node: TreeNode, path_folder: str) -> dict:
    quota_libera = settingsmodel.get_quota_disco_raw() - settingsmodel.get_size()
    return networkmodel.download_node(node, path_folder, quota_libera)


def upload_file(node: TreeNode, parent_folder_id: str) -> None:
    networkmodel.upload_node(node, parent_folder_id)


def delete_node(node_id: str) -> None:
    """Elimina un nodo in base al suo id"""
    networkmodel.delete_node(node_id)


def create_folder(folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
    return networkmodel.create_folder(folder_name, parent_folder_id)
