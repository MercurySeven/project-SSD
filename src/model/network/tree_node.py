from __future__ import annotations
from src.model.network.node import (Node, Type)
from datetime import datetime


class TreeNode:

    def __init__(self, payload: Node):
        self._payload = payload
        self._children: list[TreeNode] = []

        self._parent: TreeNode = None

    def add_node(self, node: TreeNode) -> None:
        if not self.is_directory():
            raise ValueError("TreeNode was declared as File, it's not a folder")

        node._parent = self
        self._children.append(node)

    def is_directory(self) -> bool:
        return self._payload.type == Type.Folder

    def get_name(self) -> str:
        return self._payload.name

    def get_updated_at(self) -> int:
        return self._payload.updated_at

    def __str__(self, level: int = 0):
        """Metodo per stampare tutto l'albero"""
        folder = " - Folder" if self.is_directory() else ""
        formatted_date = datetime.fromtimestamp(self.get_updated_at()).strftime("%d/%m/%Y %H:%M:%S")
        ret = " " * level + \
              f"{self.get_name()}{folder} ({self.get_updated_at()} -> {formatted_date})\n"
        for child in self._children:
            ret += child.__str__(level + 1)
        return ret

    def get_children(self) -> list:
        return self._children

    def get_payload(self) -> Node:
        return self._payload

    def get_child_from_path(self, path: str) -> TreeNode:
        for i in self._children:
            if i._payload.path == path:
                return i
