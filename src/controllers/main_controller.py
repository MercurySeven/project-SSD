from PySide6.QtCore import (QObject, Slot, QSettings)
from PySide6.QtWidgets import (QApplication)

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
        self.notification_controller = None
        self.watcher = None
        self.algoritmo = None

    def start(self):
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
            self.model, self.view.main_widget.remote_widget)
        self.settings_controller = SettingsController(
            self.model, self.view.main_widget.settings_view)
        self.notification_controller = NotificationController(self.app, self.view)

        # ALGORITMO
        self.algoritmo = DecisionEngine(self.model, self.notification_controller)
        self.algoritmo.Sg_toggle_files_update.connect(self.file_controller.Sl_toggle_files_update)
        self.file_controller._view.force_sync_button.clicked.connect(
            self.algoritmo.Sl_model_changed)
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
