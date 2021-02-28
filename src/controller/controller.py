from PySide6.QtCore import (QObject, QSettings)


from view.mainwindow import MainWindow
from model.watcher import Watcher


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.view = MainWindow()
        self.view.show()

        # Attivo il watchdog nella root definita dall'utente
        self.settings = QSettings(self)
        self.watcher = Watcher(self.settings.value("sync_path"))

        self.view.mainWidget.watchWidget.Sg_watch.connect(self.watcher.run)
