from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox

from src.controllers.main_controller import MainController
from src.model.main_model import MainModel
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel
from src.view.login_screen import LoginScreen


class LoginController:

    def __init__(self, model: MainModel, main_controller: MainController = None):
        self._net_model: NetworkModel = model.network_model
        self._set_model: SettingsModel = model.settings_model

        self.login_screen = LoginScreen(self._net_model)
        self._main_controller = main_controller

        # Connetto login vista ai due slot del controller
        self.login_screen.Sg_login_success.connect(self.Sl_logged_in)
        self.login_screen.login_button.clicked.connect(self.Sl_login)

        self._net_model.Sg_model_changed.connect(self.login_screen.Sl_model_changed)

        # Connetto il segnale di fallimento login
        self._net_model.Sg_login_failed.connect(self.Sl_login_fail)

        user = self._net_model.get_username()
        password = self._net_model.get_password()
        if len(user) > 0 and len(password) > 0:
            # Abbiamo le credenziali salvate, facciamo l'auto-login
            self._net_model.login(user, password)
            # Qui lancia una eccezione se il login fallisce
        else:
            self.start()

    def start(self) -> None:
        self._net_model.Sg_login_failed.connect(self.login_screen.Sl_login_fail)
        self.login_screen.show()

    def stop(self) -> None:
        self.login_screen.hide()
        self.login_screen.close()

    @Slot()
    def Sl_login(self):
        user = self.login_screen.get_user()
        pwd = self.login_screen.get_psw()
        self._net_model.login(user, pwd)

    @Slot()
    def Sl_logged_in(self):
        self.stop()
        if self._main_controller is not None:
            # Connetto il segnale di fallimento login al controller,
            # così in futuro può essere usato
            self._net_model.Sg_login_failed.connect(self.Sl_login_fail)
            # Avvio l'applicazione
            self._main_controller.start()

    @Slot()
    def Sl_login_fail(self):
        # Disconnetto il controller, da ora in poi solo la vista prende
        # il fail finchè essa è aperta
        self._net_model.Sg_login_failed.disconnect(self.Sl_login_fail)
        self.login_screen.Sg_login_failure.connect(self.Sl_show_error)
        self.start()

    @Slot()
    def Sl_show_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Errore nell'autenticazione con le credenziali inserite")
        msg.exec()
