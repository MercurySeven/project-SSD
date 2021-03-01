import file
import os
class Directory:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.files = os.listdir(self.path+'/'+file.name)

    def addFile(self, file):
        self.files.append(file)

    def updateListOfFiles(self):
        self.files = os.listdir(self.path+'/'+file.name)
        return self.files