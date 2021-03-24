import os
import math
from .tree_node import TreeNode
from src.model.network.node import Node, Type


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
        abs_path = os.path.join(path, name)
        if os.path.isdir(abs_path):
            get_tree_from_system(abs_path, name, parent_node)
        else:
            parent_node.add_node(_build_tree_node(abs_path, name))
    if prev_node is not None:
        prev_node.add_node(parent_node)
    return parent_node

# def search_node_from_path(tree: TreeNode, path: str) -> TreeNode:
    # for
# def _search_recursive_from_path
