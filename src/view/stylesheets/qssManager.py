from PySide2 import QtCore

'''
Da usare per settare le stylesheet dei widget
importare con
    from src.view.widgets.stylesheets.qssManager import setQss
'''


def setQss(path, self):
    self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
    with open(path, "r") as fh:
        self.setStyleSheet(fh.read())
        fh.close()
