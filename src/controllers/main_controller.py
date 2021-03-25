from os import path
from PySide6.QtCore import (QObject, Slot, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)
from src.model.main_model import MainModel
from src.model.watcher import Watcher
from src.view.login_screen import LoginScreen
from src.view.main_view import MainWindow
from .file_controller import FileController
from .notification_controller import NotificationController
from .settings_controller import SettingsController
from .widgets.sync_controller import SyncController
from src.algorithm.decision_engine import DecisionEngine


class MainController(QObject):

    def __init__(self, app: QApplication):

        # initialize settings
        self.env_settings = QSettings()
        self.app = app

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
                app.quit()

            sync_path = dialog.selectedFiles()
            if len(sync_path) == 1:
                self.env_settings.setValue("sync_path", sync_path[0])
                self.env_settings.sync()
                print("Nuova directory: " + self.env_settings.value("sync_path"))

        self.model = MainModel()

        self.login_screen = LoginScreen(self.model.network_model)
        self.login_screen.show()

        # Connetto login vista ai due slot del controller
        self.login_screen.Sg_login_success.connect(self.Sl_logged_in)
        self.login_screen.loginButton.clicked.connect(self.Sl_login)

        self.model.network_model.Sg_model_changed.connect(self.login_screen.Sl_model_changed)

        self.view = None
        self.sync_controller = None
        self.file_controller = None
        self.directory_controller = None
        self.settings_controller = None
        self.notification_icon = None
        self.watcher = None
        self.algo_v2 = None
        # TODO: Temporaneo
        self.Sl_login()

    def create_main_window(self):
        self.view = MainWindow(self.model)
        self.view.show()

        # Creazione delle View principali
        self.sync_controller = SyncController(
            self.model.sync_model, self.view.main_widget.sync_widget)
        self.file_controller = FileController(
            self.model.file_model, self.view.main_widget.files_widget)
        self.settings_controller = SettingsController(
            self.model.settings_model, self.view.main_widget.settings_view)

        self.notification_icon = NotificationController(self.app, self.view)

        # ALGORITMO V2
        self.algo_v2 = DecisionEngine(self.model.sync_model.get_state())
        self.algo_v2.start()

        # Attivo il watchdog nella root definita dall'utente
        self.watcher = Watcher()
        self.watcher.run(True)
        # Controllo se l'algoritmo era acceso l'ultima volta
        self.Sl_sync_model_changed()

        self.model.sync_model.Sg_model_changed.connect(self.Sl_sync_model_changed)

        # Ripristino il riavvio di watchdog, quando cambio path
        self.model.settings_model.Sg_model_path_changed.connect(self.Sl_path_updated)

        # connect segnali watchdog
        self.watcher.signal_event.connect(self.model.file_model.Sl_update_model)

        # Connect per cambiare le viste
        self.view.main_widget.Sg_switch_to_files.connect(self.Sl_switch_to_files)
        self.view.main_widget.Sg_switch_to_settings.connect(self.Sl_switch_to_settings)

    @Slot()
    def Sl_path_updated(self):
        self.env_settings.sync()
        self.watcher.reboot()
        if self.watcher.is_running:
            self.notification_icon.send_message("Watcher riavviato")

    @Slot()
    def Sl_sync_model_changed(self):
        state = self.model.sync_model.get_state()
        self.algo_v2.set_running(state)

    @Slot()
    def Sl_switch_to_files(self):
        self.view.main_widget.chage_current_view_to_files()

    @Slot()
    def Sl_switch_to_settings(self):
        self.view.main_widget.chage_current_view_to_settings()

    @Slot()
    def Sl_login(self):
        pwd = self.login_screen.pswField.text()
        user = self.login_screen.userField.text()
        self.model.network_model.login(user, pwd)

    @Slot()
    def Sl_logged_in(self):
        self.login_screen.hide()
        self.login_screen.close()
        self.create_main_window()
