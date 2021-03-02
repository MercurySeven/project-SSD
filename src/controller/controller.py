from PySide6.QtCore import (QObject, Slot)


from view.mainwindow import MainWindow
from model.watcher import Watcher

from time import sleep
from threading import Thread

from network.metaData import (metaData, Policy)


class Controller(QObject):

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.view = MainWindow()
        self.view.show()

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()

        self.view.mainWidget.watchWidget.Sg_watch.connect(self.Sl_watch)

        self.view.mainWidget.settingsWidget.Sg_path_changed.connect(
            self.reboot)

        self.algorithm = metaData()

        sync = Thread(target=self.background, daemon=True)
        sync.start()

    @Slot()
    def show_app(self):
        self.view.show()

    @Slot()
    def reboot(self):
        self.watcher.reboot()

    @Slot(bool)
    def Sl_watch(self, state):
        self.watcher.run(state)

    def background(self):
        while True:
            # sync do_stuff()
            if self.watcher.status():
                self.algorithm.applyChanges(
                    Policy.lastUpdate)
            sleep(20)
