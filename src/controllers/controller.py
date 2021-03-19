from threading import Thread
from time import sleep

from PySide6.QtCore import (QObject, Slot, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)

from .file_controller import FileController
from .notification_controller import NotificationController
from .settings_controller import SettingsController
from .widgets.sync_controller import SyncController
from src.model.model import Model
from src.model.watcher import Watcher
from src.network.metadata import MetaData
from src.view.main_view import MainWindow


class Controller(QObject):

    def __init__(self, app: QApplication, parent=None):
        super(Controller, self).__init__(parent)

        # initialize settings
        self.env_settings = QSettings()

        # Controlliamo se l'utente ha già settato il PATH della cartella
        if not self.env_settings.value("sync_path"):
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
            dialog.setOption(QFileDialog.ShowDirsOnly)
            dialog.setOption(QFileDialog.DontResolveSymlinks)

            # L'utente non ha selezionato la cartella
            if not dialog.exec_():
                self.env_settings.setValue("sync_path", None)
                app.quit()

            sync_path = dialog.selectedFiles()
            if len(sync_path) == 1:
                self.env_settings.setValue("sync_path", sync_path[0])
                self.env_settings.sync()
                print("Nuova directory: " + self.env_settings.value("sync_path"))

        self.model = Model()
        self.view = MainWindow(self.model)
        self.view.show()

        # Creazione delle View principali
        self.sync_controller = SyncController(
            self.model.sync_model, self.view.main_widget.sync_widget)
        self.file_controller = FileController(
            self.model.files_model, self.view.main_widget.files_widget)
        self.settings_controller = SettingsController(
            self.model.settings_model, self.view.main_widget.settings_view)

        # Non so se ci vada il parent su Notification...
        self.notification_icon = NotificationController(app, parent)
        self.notification_icon.Sg_show_app.connect(lambda: self.view.show())

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()
        # Controllo se l'algoritmo era acceso l'ultima volta
        self.Sl_sync_model_changed()

        self.model.sync_model.Sg_model_changed.connect(self.Sl_sync_model_changed)

        # Ripristino il riavvio di watchdog, quando cambio path
        self.model.settings_model.Sg_model_changed.connect(self.Sl_path_updated)

        # Connect per cambiare le viste
        self.view.main_widget.Sg_switch_to_files.connect(self.Sl_switch_to_files)
        self.view.main_widget.Sg_switch_to_settings.connect(self.Sl_switch_to_settings)

        # Parte dell'algoritmo
        self.algorithm = MetaData(self.env_settings.value("sync_path"))

        sync = Thread(target=self.background, daemon=True)
        sync.setName("algorithm's thread")
        sync.start()

    @Slot()
    def Sl_update_size(self):
        """permette l'aggiornamento automatico della quota utilizzata"""
        self.view.mainWidget.settings_view.Sl_update_used_quota(
            self.algorithm.get_size())

    @Slot()
    def Sl_path_updated(self):
        new_path = self.view.mainWidget.settings_view.settings_model.get_path()
        self.env_settings.sync()
        self.algorithm.set_directory(new_path)
        self.watcher.reboot()
        self.notification_icon.send_message("Watcher riavviato")

    @Slot()
    def Sl_sync_model_changed(self):
        state = self.model.sync_model.get_state()
        self.watcher.run(state)

    def background(self):
        while True:
            # sync do_stuff()
            if self.watcher.status():
                self.algorithm.apply_changes()
            sleep(5)

    @Slot()
    def Sl_switch_to_files(self):
        self.view.main_widget.chage_current_view_to_files()

    @Slot()
    def Sl_switch_to_settings(self):
        self.view.main_widget.chage_current_view_to_settings()
