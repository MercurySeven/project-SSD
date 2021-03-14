from PySide6.QtCore import (QObject, Slot, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)

from view import MainWindow
from model import Watcher

from time import sleep
from threading import Thread

from network import (MetaData)
from .notification_icon import (NotificationIconController)


class Controller(QObject):

    def __init__(self, app: QApplication, parent=None):
        super(Controller, self).__init__(parent)

        # initialize settings
        env_settings = QSettings()
        # Controlliamo se l'utente ha già settato il PATH della cartella
        if not env_settings.value("sync_path"):
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
            dialog.setOption(QFileDialog.ShowDirsOnly)
            dialog.setOption(QFileDialog.DontResolveSymlinks)

            # L'utente non ha selezionato la cartella
            if not dialog.exec_():
                env_settings.setValue("sync_path", None)
                app.quit()

            sync_path = dialog.selectedFiles()
            if (len(sync_path) == 1):
                env_settings.setValue("sync_path", sync_path[0])
                env_settings.sync()
                print("Nuova directory: " + env_settings.value("sync_path"))

        self.view = MainWindow()
        self.view.show()

        # Non so se ci vada il parent su Notification...
        self.notification_icon = NotificationIconController(app, parent)
        self.notification_icon.Sg_show_app.connect(lambda: self.view.show())

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()

        self.view.mainWidget.watchWidget.Sg_watch.connect(self.Sl_watch)

        # self.view.mainWidget.settingsWidget.Sg_path_changed.connect(
        #     self.reboot)

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
    def reboot(self):
        self.env_settings.sync()
        self.algorithm.set_directory(self.env_settings.value("sync_path"))
        self.view.mainWidget.settingsWidget.Sl_update_used_quota(
            self.algorithm.get_size())
        self.watcher.reboot()
        self.notification_icon.send_message("Watcher riavviato")

    @Slot(bool)
    def Sl_watch(self, state):
        self.watcher.run(state)

    def background(self):
        while True:
            # sync do_stuff()
            if self.watcher.status():
                self.algorithm.apply_changes()
            sleep(5)
