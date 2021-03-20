from __future__ import annotations
from src.model.network.node import (Node, Type)
from datetime import datetime


class TreeNode:

    def __init__(self, payload: Node):
        self._name = payload.name
        self._updated_at = payload.updated_at
        self._type = payload.type
        self._children: list[TreeNode] = []

    def add_node(self, node: TreeNode) -> None:
        if self._type == Type.File:
            raise ValueError("TreeNode was declared as File, it's not a folder")

        self._children.append(node)
        self._updated_at = max(self._updated_at, node._updated_at)

    def is_directory(self) -> bool:
        return self._type == Type.Folder

    def __str__(self, level: int = 0):
        """Metodo per stampare tutto l'albero"""
        folder = " - Folder" if self.is_directory() else ""
        formatted_date = datetime.fromtimestamp(self._updated_at).strftime("%d/%m/%Y %H:%M:%S")
        ret = " " * level + f"{self._name}{folder} ({self._updated_at} -> {formatted_date})\n"
        for child in self._children:
            ret += child.__str__(level + 1)
        return ret
