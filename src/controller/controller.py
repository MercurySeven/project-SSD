from PySide6.QtCore import (QObject, Slot)


from view.mainwindow import MainWindow
from model.watcher import Watcher
from model.file import File
from model.directory import Directory


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.view = MainWindow()
        self.view.show()

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()

        self.view.mainWidget.watchWidget.Sg_watch.connect(self.watcher.run)

    def showFiles(self):
        dir = Directory()

    @Slot()
    def show_app(self):
        self.view.show()
