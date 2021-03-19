
import os

from .file import File
from datetime import datetime


class Directory:

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.files = {}
        self.dirs = {}
        self.update_list_of_content()

    def add_file(self, file: File) -> None:
        self.files.update({file.get_name(): file})

    def update_list_of_content(self) -> None:
        if not self.path or not os.path.isdir(self.path):
            return
        restore_path = os.getcwd()
        with os.scandir(self.path) as dir_entries:
            os.chdir(self.path)  # punto critico dell'app!
            for entry in dir_entries:
                created_at = os.stat(entry.name).st_ctime
                updated_at = os.stat(entry.name).st_mtime
                if os.path.isfile(entry.name):
                    file = File(entry.name,
                                self.__convert_to_date(created_at),
                                self.__convert_to_date(updated_at),
                                self.define_type(entry.name),
                                str(os.stat(entry.name).st_size),
                                "stato file")
                    self.files.update({file.get_name(): file})
                else:
                    path = os.path.join(str(os.path), entry.name)
                    self.dirs.update({
                        str(entry.name): Directory(entry.name, path)
                    })
        os.chdir(restore_path)

    def __convert_to_date(self, date: float) -> str:
        return datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")

    def define_type(self, file_type: str) -> str:
        pos = file_type.rfind('.')
        return file_type[(pos + 1):]
