
import os
from src.model.file import File


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
                file = File(entry.name, os.stat(entry.name).st_ctime, os.stat(entry.name).st_mtime_ns, "content_type", os.stat(entry.name).st_size, " ")
                self.files.append(file)
                print(file.getName() + " "+ file.getType())
