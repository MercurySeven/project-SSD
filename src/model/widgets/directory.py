import os

from src.model.widgets.file import File
from datetime import datetime
from src.model.network.node import Type


class Directory:

    def __init__(self, name, path, creation_date, tree):
        self._name = name
        self._path = path
        self._files = []
        self._dirs = []
        self._creation_date = creation_date
        self._last_modified_date = creation_date
        self._node = tree
        self.update_list_of_content()

    def add_file(self, file: File) -> None:
        self._files.update({file.get_name(): file})

    def update_list_of_content(self) -> None:
        self._files.clear()
        self._dirs.clear()
        if not self._path or not os.path.isdir(self._path):
            return
        content = self._node.get_children()
        for entry in content:
            if entry.get_payload().type == Type.File:
                file = File(entry.get_payload().name,
                            self.__convert_to_date(entry.get_payload().created_at),
                            self.__convert_to_date(entry.get_payload().updated_at),
                            self.define_type(entry.get_payload().name),
                            str(os.stat(entry.get_payload().path).st_size),
                            "stato file")
                self._files.append(file)
            else:
                self._dirs.append(
                    Directory(entry.get_payload().name, entry.get_payload().path, "oggi", entry)
                )

    def __convert_to_date(self, date: float) -> str:
        return datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")

    def define_type(self, file_type: str) -> str:
        pos = file_type.rfind('.')
        return file_type[(pos + 1):]

    def get_name(self) -> str:
        return self._name

    def get_creation_date(self):
        return self._creation_date

    def get_last_modified_date(self):
        return self._last_modified_date

    def get_path(self) -> str:
        return self._path

    def set_path(self, path) -> None:
        self._path = path

    def set_name(self, name) -> None:
        self._name = name

    @property
    def dirs(self):
        return self._dirs

    @property
    def files(self):
        return self._files
