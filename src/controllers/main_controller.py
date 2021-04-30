from os import path

from PySide6.QtCore import (QObject, Slot, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)

from src.algorithm.decision_engine import DecisionEngine
from src.model.main_model import MainModel
from src.model.watcher import Watcher
from src.view.main_view import MainWindow
from .file_controller import FileController
from .notification_controller import NotificationController
from .settings_controller import SettingsController
from .widgets.sync_controller import SyncController
from .remote_file_controller import RemoteFileController


class MainController(QObject):

    def __init__(self, app: QApplication, model: MainModel):

        # initialize settings
        self.env_settings = QSettings()
        self.app = app
        self.model = model
        self.view = None
        self.sync_controller = None
        self.file_controller = None
        self.remote_file_controller = None
        self.settings_controller = None
        self.notification_icon = None
        self.watcher = None
        self.algoritmo = None

    def start(self):
        # Controlliamo se l'utente ha già settato il PATH della cartella
        check_path = self.env_settings.value("sync_path")
        if not check_path or not path.isdir(check_path):
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
            dialog.setOption(QFileDialog.ShowDirsOnly)
            dialog.setOption(QFileDialog.DontResolveSymlinks)

            # L'utente non ha selezionato la cartella
            if not dialog.exec_():
                self.env_settings.setValue("sync_path", None)
                self.app.quit()

            sync_path = dialog.selectedFiles()
            if len(sync_path) == 1:
                self.env_settings.setValue("sync_path", sync_path[0])
                self.env_settings.sync()
                print("Nuova directory: " + self.env_settings.value("sync_path"))

        # Create main window
        self.model.remote_file_model.set_network_model(self.model.network_model)
        self.view = MainWindow(self.model)
        self.view.show()

        # Creazione delle View principali
        self.sync_controller = SyncController(
            self.model.sync_model, self.view.main_widget.sync_widget)
        self.file_controller = FileController(
            self.model.file_model, self.view.main_widget.files_widget)
        self.remote_file_controller = RemoteFileController(
            self.model.remote_file_model, self.view.main_widget.remote_widget)
        self.settings_controller = SettingsController(
            self.model, self.view.main_widget.settings_view)
        self.notification_icon = NotificationController(
            self.app, self.view, self.model.network_model.get_username())

        # ALGORITMO
        # TODO: Da spostare nel main model
        self.algoritmo = DecisionEngine(self.model, self.notification_icon)
        self.algoritmo.start()

        self.model.settings_model.Sg_model_changed.connect(self.algoritmo.Sl_model_changed)

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()
        self.watcher.run(True)
        # Controllo se l'algoritmo era acceso l'ultima volta
        self.Sl_sync_model_changed()

        self.model.sync_model.Sg_model_changed.connect(self.Sl_sync_model_changed)

        # Ripristino il riavvio di watchdog, quando cambio path
        self.model.settings_model.Sg_model_path_changed.connect(self.Sl_path_updated)

        # Connect segnali watchdog
        self.watcher.signal_event.connect(self.model.file_model.Sl_update_model)
        self.watcher.signal_event.connect(
            self.view.main_widget.settings_view.set_quota_disk_widget.Sl_model_changed)

        # Connect per cambiare le viste
        self.view.main_widget.Sg_switch_to_files.connect(self.Sl_switch_to_files)
        self.view.main_widget.Sg_switch_to_remote.connect(self.Sl_switch_to_remote)
        self.view.main_widget.Sg_switch_to_settings.connect(self.Sl_switch_to_settings)

    @Slot()
    def Sl_path_updated(self):
        self.env_settings.sync()
        self.watcher.reboot()
        self.notification_icon.send_message("Watcher riavviato")

    @Slot()
    def Sl_sync_model_changed(self):
        state = self.model.sync_model.get_state()
        self.algoritmo.set_running(state)

    @Slot()
    def Sl_switch_to_files(self):
        self.view.main_widget.chage_current_view_to_files()

    @Slot()
    def Sl_switch_to_remote(self):
        self.view.main_widget.chage_current_view_to_remote()

    @Slot()
    def Sl_switch_to_settings(self):
        self.view.main_widget.chage_current_view_to_settings()
