from enum import Enum


class Type(Enum):
    File = 1
    Folder = 2


class Node:
    """Classe che verrà usata per contenere le info dei file"""

    def __init__(self,
                 id: str,
                 name: str,
                 type: Type,
                 created_at: int,
                 updated_at: int,
                 path: str = None):
        # Un nodo con path = None è un nodo cloud
        self.id: str = id
        self.name: str = name
        self.type: Type = type
        self.created_at: int = created_at
        self.updated_at: int = updated_at
        self.path = path
