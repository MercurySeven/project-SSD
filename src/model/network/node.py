from enum import Enum


class Type(Enum):
    File = 1
    Folder = 2


class Node:
    """Classe che verrà usata per contenere le info delle API Zextras"""

    def __init__(self,
                 id: str,
                 name: str,
                 type: Type,
                 created_at: int,
                 updated_at: int):

        self.id: str = id
        self.name: str = name
        self.type: Type = type
        self.created_at: int = created_at
        self.updated_at: int = updated_at


class File(Node):
    def __init__(self,
                 id: str,
                 name: str,
                 type: Type,
                 created_at: int,
                 updated_at: int,
                 size: int):
        super().__init__(id, name, type, created_at, updated_at)
        self.size: int = size
