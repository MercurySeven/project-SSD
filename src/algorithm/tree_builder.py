import os
import math
import pickle
import sys
import ctypes
from src.model.algorithm.tree_node import TreeNode
from src.model.algorithm.node import Node, Type
from typing import Optional
from src.model.network_model import NetworkModel


FILE_DUMP_NAME = "client_dump.mer"
FOLDER_NAME = ".zextrasdrive"

black_list = [FOLDER_NAME, ".DS_Store"]
networkmodel: NetworkModel = None


def set_model(model: NetworkModel) -> None:
    global networkmodel
    networkmodel = model


def _build_tree_node(path: str, name: str) -> TreeNode:
    """Costruisce un TreeNode a partire dal path"""
    id = "CLIENT_NODE"
    # name = os.path.basename(path)
    type = Type.Folder if os.path.isdir(path) else Type.File
    created_at = math.trunc(os.stat(path).st_ctime)
    updated_at = math.trunc(os.stat(path).st_mtime)

    return TreeNode(Node(id, name, type, created_at, updated_at, path))


def get_tree_from_system(path: str,
                         root_name: str = "ROOT",
                         prev_node: TreeNode = None) -> TreeNode:
    """Funzione ricorsiva per costruire l'albero dato un path"""
    parent_node = _build_tree_node(path, root_name)
    for name in os.listdir(path):
        if name not in black_list:
            abs_path = os.path.join(path, name)
            if os.path.isdir(abs_path):
                get_tree_from_system(abs_path, name, parent_node)
            else:
                parent_node.add_node(_build_tree_node(abs_path, name))

    if prev_node is not None:
        prev_node.add_node(parent_node)
    return parent_node


def _create_node_from_dict(dict: str) -> TreeNode:
    """Costruisce un TreeNode a partire dal dict"""
    id = dict["id"]
    name = dict["name"]
    type = Type.File if dict["type"] == "File" else Type.Folder
    created_at = math.trunc(dict["created_at"] / 1000)
    updated_at = math.trunc(dict["updated_at"] / 1000)
    return TreeNode(Node(id, name, type, created_at, updated_at))


def get_tree_from_node_id(node_id: str = "LOCAL_ROOT") -> TreeNode:
    """Funzione ricorsiva per costruire l'albero remodo dato un node_id"""
    json = networkmodel.get_content_from_node(node_id)
    networkmodel.raise_for_status()
    folder = _create_node_from_dict(json["getNode"])
    for _file in json["getNode"]["children"]:
        new_node = _create_node_from_dict(_file)

        if new_node.is_directory():
            # Fai chiamata web per il nuovo nodo
            folder_tree_node = get_tree_from_node_id(new_node._payload.id)
            folder.add_node(folder_tree_node)
        else:
            folder.add_node(new_node)

    return folder


def dump_client_filesystem(path: str) -> None:
    """Crea lo snapshot dell'albero locale e lo salva nel path passato, all'interno di una
        cartella nascosta"""
    hidden_folder_path = _create_hidden_folder(path)
    file_path = os.path.join(hidden_folder_path, FILE_DUMP_NAME)
    client_tree = get_tree_from_system(path)
    with open(file_path, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(client_tree, f, pickle.HIGHEST_PROTOCOL)


def read_dump_client_filesystem(path: str) -> Optional[TreeNode]:
    """Restituisce l'albero locale salvato nello snapshot"""
    hidden_folder_path = _create_hidden_folder(path)
    file_path = os.path.join(hidden_folder_path, FILE_DUMP_NAME)
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                data: TreeNode = pickle.load(f)
            return data
        except Exception:
            return None
    else:
        return None


def _create_hidden_folder(path: str) -> str:
    """Crea una cartella nascosta dove mettere i vari file"""
    folder_path = os.path.join(path, FOLDER_NAME)
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
        if sys.platform == "win32":
            try:
                ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)  # Hide folder
            except OSError as e:
                print(e)
    return folder_path
