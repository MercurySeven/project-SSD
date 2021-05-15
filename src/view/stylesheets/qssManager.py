import os
import sys
from PySide6 import QtCore
from src import assets_path

'''
Da usare per settare le stylesheet dei widget
importare con
    from src.view.widgets.stylesheets.qssManager import setQss
'''


def setQss(path: str, self) -> None:
    self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
    with open(resource_path(path), "r") as fh:
        self.setStyleSheet(fh.read())
        fh.close()


def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, assets_path.ASSETS_PATH, relative_path)
