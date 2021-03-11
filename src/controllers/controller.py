from PySide6.QtCore import (QObject, Slot, QSettings)

from view import MainWindow
from model import Watcher

from time import sleep
from threading import Thread

from network import (MetaData, Policy)


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

        self.view.mainWidget.settingsWidget.Sg_policy_client.connect(
            lambda: self.Sl_change_policy(Policy.Client))
        self.view.mainWidget.settingsWidget.Sg_policy_manuale.connect(
            lambda: self.Sl_change_policy(Policy.Manual))

        self.env_settings = QSettings()
        self.algorithm = MetaData(self.env_settings.value("sync_path"))

        # imposto le dimensioni della quota disco
        self.view.mainWidget.settingsWidget.Sl_update_used_quota(
            self.algorithm.get_size())

        sync = Thread(target=self.background, daemon=True)
        sync.setName("algorithm's thread")
        sync.start()

    @Slot()
    def Sl_update_size(self):
        """permette l'aggiornamento automatico della quota utilizzata"""
        self.view.mainWidget.settingsWidget.Sl_update_used_quota(
            self.algorithm.get_size())

    @Slot()
    def show_app(self):
        self.view.show()

    @Slot()
    def reboot(self):
        self.env_settings.sync()
        self.algorithm.set_directory(self.env_settings.value("sync_path"))
        self.view.mainWidget.settingsWidget.Sl_update_used_quota(
            self.algorithm.get_size())
        self.watcher.reboot()

    @Slot()
    def Sl_change_policy(self, policy: Policy):
        self.algorithm.change_policy(policy)

    @Slot(bool)
    def Sl_watch(self, state):
        self.watcher.run(state)

    def background(self):
        while True:
            # sync do_stuff()
            if self.watcher.status():
                self.algorithm.apply_changes()
            sleep(5)