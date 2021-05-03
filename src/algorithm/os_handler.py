import os
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel

network_model: NetworkModel = None
settings_model: SettingsModel = None


def set_network_model(net_model: NetworkModel) -> None:
    global network_model
    network_model = net_model


def set_settings_model(set_model: SettingsModel) -> None:
    global settings_model
    settings_model = set_model


def download_folder(node: TreeNode, path: str) -> list[dict]:
    """Il nodo rappresenta la cartella che non esiste,
    ritorna i risultati dei download che sono stati fatti"""
    path_folder = os.path.join(path, node.get_name())
    os.mkdir(path_folder)

    download_operations_list = []
    for _node in node.get_children():
        if _node.is_directory():
            result = download_folder(_node, path_folder)
            download_operations_list.extend(result)
        else:
            result = download_file(_node, path_folder)
            download_operations_list.append(result)
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
    quota_libera = settings_model.get_quota_libera()
    return network_model.download_node(node, path_folder, quota_libera)


def upload_file(node: TreeNode, parent_folder_id: str) -> None:
    network_model.upload_node(node, parent_folder_id)


def delete_node(node_id: str) -> None:
    """Elimina un nodo in base al suo id"""
    network_model.delete_node(node_id)


def create_folder(folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
    return network_model.create_folder(folder_name, parent_folder_id)
