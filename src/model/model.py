import os
import glob
from distutils.dir_util import remove_tree
from typing import Generator

# TODO: provvisoria


class Model:
    def __init__(self, remote: str, local: str):

        # set remote and local path
        self.remote = remote
        self.local = local

        # returns time of the last change in the folder
        self.last_change = lambda path: os.path.getmtime(path)

    def remote_content(self) -> Generator[str, None, None]:
        """fake remote call
        return the contents of the remote directory"""
        return self.content(self.remote)

    def local_content(self) -> Generator[str, None, None]:
        """return the contents of the local directory"""
        return self.content(self.local)

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
