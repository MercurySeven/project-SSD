import os
from PySide6 import QtCore

'''
Da usare per settare le stylesheet dei widget
importare con
    from view.widget.stylesheets.qssManager import setQss
'''


def setQss(path, self):
    self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, path)
    with open(my_file, "r") as fh:
        self.setStyleSheet(fh.read())
        fh.close()
