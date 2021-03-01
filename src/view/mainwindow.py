from PySide6.QtWidgets import (QMainWindow)
from PySide6.QtGui import (QIcon)
from PySide6.QtCore import QSettings

from view.widget.mainwidget import MainWidget

import sys

from src.view.stylesheets.qssManager import setQss


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        # self.label = QLabel("MainWindow", self)
        # self.label.setAlignment(Qt.AlignCenter)

        # initialize settings
        self.settings = QSettings(self)

        # self.settings.setValue("sync_path", None)  # debug

        # Controlliamo se l'utente ha già settato il PATH della cartella
        if not self.settings.value("sync_path"):
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
            dialog.setOption(QFileDialog.ShowDirsOnly)
            dialog.setOption(QFileDialog.DontResolveSymlinks)

            # L'utente non ha selezionato la cartella
            if not dialog.exec_():
                self.settings.setValue("sync_path", None)
                sys.exit()

            sync_path = dialog.selectedFiles()
            if (len(sync_path) == 1):
                self.settings.setValue("sync_path", sync_path[0])
                print("Nuova directory: " + self.settings.value("sync_path"))
                # self.settings.sync() # save

        # widgets
        self.mainWidget = MainWidget(self)

        # Non più necessario ma da controllare
        # create layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.mainWidget)
        # self.setLayout(layout)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.mainWidget)

        # style
        self.resize(1200, 800)

        setQss("style.qss", self)
