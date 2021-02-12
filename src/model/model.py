from distutils.dir_util import remove_tree
from model.client import API_Client
from settings import Settings
from typing import Generator
import glob
import os


# TODO: provvisoria
class Model:
    def __init__(self, remote: str, local: str):

        # set remote and local path
        self.remote = os.path.join(Settings['REAL_PATH'], remote)
        self.local = os.path.join(Settings['REAL_PATH'], local)

        self.api = API_Client(Settings['HOST'], Settings['PORT'])

        # returns time of the last change in the folder
        self.last_change = lambda path: os.path.getmtime(path)

    def remote_content(self) -> list:
        """fake remote call
        return the contents of the remote directory"""

        query = '{content(path: "REMOTE/")}'

        # fak api call
        response = self.api.get_content(query)
        return response['content']

    def local_content(self) -> list:
        """return the contents of the local directory"""
        return list(self.content(self.local))

    def remote_last_change(self) -> float:
        """fake remote call
        return the last change time of the remote directory"""
        return self.last_change(self.remote)

    def local_last_change(self) -> float:
        """return the last change time of the remote directory"""
        return self.last_change(self.local)

    def remote_clear(self) -> None:
        self.clear(self.remote)

    def local_clear(self) -> None:
        self.clear(self.local)

    def content(self, path: str) -> Generator[str, None, None]:
        """returns the contents of the folder"""
        for root, dirs, files in os.walk(path):
            root = root.replace(path, "")
            for name in dirs + files:
                yield os.path.join(root, name)

    # remove the contents of the folder
    def clear(self, root: str) -> None:
        for path in glob.glob(root+'*'):
            remove_tree(path) if os.path.isdir(path) else os.remove(path)
