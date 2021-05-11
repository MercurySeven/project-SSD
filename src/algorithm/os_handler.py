import os
from typing import Optional
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel
from . import tree_builder

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

    # Controlliamo se la cartella ha dei nodi da scaricare
    file_node_list = settings_model.get_sync_list()
    res = check_node_in_nodelist(node, file_node_list)

    download_operations_list = []

    if res:
        path_folder = os.path.join(path, node.get_name())
        os.mkdir(path_folder)

        for _node in node.get_children():
            if _node.is_directory():
                result = download_folder(_node, path_folder)
                download_operations_list.extend(result)
            else:
                result = download_file(_node, path_folder)
                if result is not None:
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


def download_file(node: TreeNode, path_folder: str) -> Optional[dict]:
    node_id = node.get_payload().id
    if settings_model.is_id_in_sync_list(node_id):
        quota_libera = settings_model.get_quota_libera()
        return network_model.download_node(node, path_folder, quota_libera)
    else:
        return None


def upload_file(node: TreeNode, parent_folder_id: str) -> None:
    network_model.upload_node(node, parent_folder_id)


def delete_node(node_id: str, is_file: bool) -> bool:
    """Elimina un nodo in base al suo id, ritorna se l'eliminazione è avvenuta o no"""
    file_node_list = settings_model.get_sync_list()
    if is_file:
        if node_id in file_node_list:
            network_model.delete_node(node_id)
            return True
        return False
    else:
        # Se un nodo all'interno della cartella è nella whitelist allora cancelliamo la cartella
        # dal server
        tree: TreeNode = tree_builder.get_tree_from_node_id(node_id)
        result = check_node_in_nodelist(tree, file_node_list)
        if result:
            network_model.delete_node(node_id)
        return result


def check_node_in_nodelist(tree: TreeNode, file_node_list: list) -> bool:
    # Per velocizzarlo di più forse è meglio ordinare i children mettendo prima i files
    for node in tree.get_children():
        if node.is_directory():
            # Se la cartella analizzata ha un nodo positivo,
            # ritorna True altrimenti guardiamo gli altri nodi
            if check_node_in_nodelist(node, file_node_list):
                return True
        else:
            if node.get_payload().id in file_node_list:
                return True
    return False


def create_folder(folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
    return network_model.create_folder(folder_name, parent_folder_id)
