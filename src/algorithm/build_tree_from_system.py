import os
import math
from .tree_node import TreeNode
from src.model.network.node import Node, Type


def get_last_time(_file: str) -> int:
    return math.trunc(os.stat(_file).st_mtime)


def build_tree_node(path: str, name: str) -> TreeNode:
    """Costruisce un TreeNode a partire dal path"""
    id = "LOCAL FILE"
    # name = os.path.basename(path)
    type = Type.Folder if os.path.isdir(path) else Type.File
    created_at = math.trunc(os.stat(path).st_ctime)
    updated_at = math.trunc(os.stat(path).st_mtime)

    return TreeNode(Node(id, name, type, created_at, updated_at))


def get_tree_from_system(path: str,
                         root_name: str = "LOCAL_ROOT",
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
