import os

from src.model.widgets.file import File
from datetime import datetime


class Directory:

    def __init__(self, name, path, creation_date):
        self._name = name
        self._path = path
        self._files = []
        self._dirs = []
        self._creation_date = creation_date
        self._last_modified_date = creation_date
        self.update_list_of_content()

    def add_file(self, file: File) -> None:
        self._files.update({file.get_name(): file})

    def update_list_of_content(self) -> None:
        if not self._path or not os.path.isdir(self._path):
            return
        with os.scandir(self._path) as dir_entries:
            self._files.clear()
            self._dirs.clear()
            for entry in dir_entries:
                entry_path = os.path.join(self._path, entry.name)
                created_at = os.stat(entry_path).st_ctime
                updated_at = os.stat(entry_path).st_mtime
                if os.path.isfile(entry_path):
                    file = File(entry.name,
                                self.__convert_to_date(created_at),
                                self.__convert_to_date(updated_at),
                                self.define_type(entry.name),
                                str(os.stat(entry_path).st_size),
                                "stato file")
                    self._files.append(file)
                else:
                    self._dirs.append(
                        Directory(entry.name, entry_path, "oggi")
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
