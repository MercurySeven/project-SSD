from PySide6.QtCore import (QObject, Slot, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)
from src.view.main_view import MainWindow
from src.model.watcher import Watcher

from time import sleep
from threading import Thread

from src.network.metadata import MetaData
from .notification_controller import NotificationController


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
        self.notification_icon = NotificationController(app, parent)
        self.notification_icon.Sg_show_app.connect(lambda: self.view.show())

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()
        self.Sl_sync_model_changed()
        self.view.mainWidget.sync_model.Sg_model_changed.connect(self.Sl_sync_model_changed)

        # Ripristino il riavvio di watchdog, quando cambio path
        self.view.mainWidget.settingsWidget.settings_model.Sg_model_changed.connect(
            self.Sl_path_updated)

        self.env_settings = QSettings()
        self.algorithm = MetaData(self.env_settings.value("sync_path"))

        sync = Thread(target=self.background, daemon=True)
        sync.setName("algorithm's thread")
        sync.start()

    @Slot()
    def Sl_update_size(self):
        """permette l'aggiornamento automatico della quota utilizzata"""
        self.view.mainWidget.settingsWidget.Sl_update_used_quota(
            self.algorithm.get_size())

    @Slot()
    def Sl_path_updated(self):
        new_path = self.view.mainWidget.settingsWidget.settings_model.get_path()
        self.env_settings.sync()
        self.algorithm.set_directory(new_path)
        self.watcher.reboot()
        self.notification_icon.send_message("Watcher riavviato")

    @Slot()
    def Sl_sync_model_changed(self):
        state = self.view.mainWidget.sync_model.get_state()
        self.watcher.run(state)

    def background(self):
        while True:
            # sync do_stuff()
            if self.watcher.status():
                self.algorithm.apply_changes()
            sleep(5)
