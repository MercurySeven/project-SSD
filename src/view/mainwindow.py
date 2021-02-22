from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget, QMainWindow,
                               QFileDialog)

from view.widget.mainwidget import MainWidget


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.label = QLabel("MainWindow", self)
        self.label.setAlignment(Qt.AlignCenter)

        # initialize settings
        self.settings = QSettings(self)

        # settings.setValue("sync/path", None)  # debug

        if not self.settings.value("sync/path"):
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
            dialog.setOption(QFileDialog.ShowDirsOnly)
            dialog.setOption(QFileDialog.DontResolveSymlinks)

            if dialog.exec_():
                sync_path = dialog.selectedFiles()
                self.settings.setValue("sync/path", sync_path)
                # self.settings.sync() # save
        
        print(self.settings.value("sync/path"))  # debug

        # widgets
        self.mainWidget = MainWidget(self)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.mainWidget)
        self.setLayout(layout)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.mainWidget)

        # style
        self.resize(800, 600)
