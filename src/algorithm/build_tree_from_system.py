import os
import math
from .tree_node import TreeNode
from src.model.network.node import Node, Type
from src.network.api import API


def build_tree_node(path: str, name: str) -> TreeNode:
    """Costruisce un TreeNode a partire dal path"""
    id = "CLIENT_NODE"
    # name = os.path.basename(path)
    type = Type.Folder if os.path.isdir(path) else Type.File
    created_at = math.trunc(os.stat(path).st_ctime)
    updated_at = math.trunc(os.stat(path).st_mtime)

    return TreeNode(Node(id, name, type, created_at, updated_at))


def get_tree_from_system(path: str,
                         root_name: str = "ROOT",
                         prev_node: TreeNode = None) -> TreeNode:
    """Funzione ricorsiva per costruire l'albero dato un path"""
    parent_node = build_tree_node(path, root_name)
    for f in os.listdir(path):
        abs_path = os.path.join(path, f)
        name = root_name + "/" + f
        if os.path.isdir(abs_path):
            get_tree_from_system(abs_path, name, parent_node)
        else:
            parent_node.add_node(build_tree_node(abs_path, name))

    if prev_node is not None:
        prev_node.add_node(parent_node)
    return parent_node


def create_node_from_dict(dict: str) -> TreeNode:
    """Costruisce un TreeNode a partire dal dict"""
    """
        # Esempio
        "id": "7183b314-a79a-461b-83d7-7526d279e4ac",
        "name": "File sincronizzato.txt",
        "created_at": 1615406876000,
        "updated_at": 1615495212000,
        "type": "File",
        "size": 50
    """
    id = dict["id"]
    name = dict["name"]
    type = Type.File if dict["type"] == "File" else Type.Folder
    created_at = math.trunc(dict["created_at"] / 1000)
    updated_at = math.trunc(dict["updated_at"] / 1000)
    return TreeNode(Node(id, name, type, created_at, updated_at))


def get_tree_from_drive_rec(json: str) -> TreeNode:
    folder = create_node_from_dict(json)
    for _file in json["children"]:
        new_node = create_node_from_dict(_file)
        folder.add_node(new_node)
    return folder


def get_tree_from_drive(email: str, password: str):
    api = API(email, password)
    json = api.get_content_from_node()
    obj = json["getNode"]
    node = get_tree_from_drive_rec(obj)
    print(node._children[0]._payload.id)
