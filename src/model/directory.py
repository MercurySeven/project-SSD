
import os
from src.model.file import File
from datetime import datetime

class Directory:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.files = []
        self.updateListOfFiles()

    def addFile(self, file):
        self.files.append(file)

    def updateListOfFiles(self):
        with os.scandir(self.path) as dir_entries:
            os.chdir(self.path)
            for entry in dir_entries:
                dir = str(self.path) + '/' + entry.name
                # content_type = magic.from_file( dir, mime=True)
                file = File(entry.name,
                            datetime.fromtimestamp(os.stat(entry.name).st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                            datetime.fromtimestamp(os.stat(entry.name).st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                            self.defineType(entry.name),
                            str(os.stat(entry.name).st_size)+" Byte", os.stat(entry.name).st_size)
                self.files.append(file)

    def defineType(self, str):
        pos = str.rfind('.')
        return str[(pos+1):]
