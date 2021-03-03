
import os
from model.file import File
from datetime import datetime


class Directory:

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.files = []
        self.update_list_of_files()

    def add_file(self, file):
        self.files.append(file)

    def update_list_of_files(self):
        restore_path = os.getcwd()
        with os.scandir(self.path) as dir_entries:
            os.chdir(self.path)  # punto critico dell'app!
            for entry in dir_entries:
                dir = os.path.join(str(self.path), entry.name)
                file = File(entry.name,
                            datetime.fromtimestamp(os.stat(entry.name).st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                            datetime.fromtimestamp(os.stat(entry.name).st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                            self.define_type(entry.name),
                            str(os.stat(entry.name).st_size), os.stat(entry.name).st_size)
                self.files.append(file)
        os.chdir(restore_path)

    def define_type(self, str):
        pos = str.rfind('.')
        return str[(pos + 1):]