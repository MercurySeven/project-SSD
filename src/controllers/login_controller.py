from PySide6.QtCore import Slot

from src.controllers.main_controller import MainController
from src.model.main_model import MainModel
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel
from src.view.login_screen import LoginScreen


class LoginController:

    def start(self):
        self.login_screen.show()

    def __init__(self, model: MainModel, main_controller: MainController = None):
        self._net_model: NetworkModel = model.network_model
        self._set_model: SettingsModel = model.settings_model

        self.login_screen = LoginScreen(self._net_model)
        self._main_controller = main_controller

        # Connetto login vista ai due slot del controller
        self.login_screen.Sg_login_success.connect(self.Sl_logged_in)
        self.login_screen.login_button.clicked.connect(self.Sl_login)

        self._net_model.Sg_model_changed.connect(self.login_screen.Sl_model_changed)
        self.login_screen.login_button.click()

        # Prendo cookie di sessione salvato nella variabile d'ambiente
        self._set_model.get_cookie()
        cookie = self._set_model.get_cookie()
        # Purgo valori scorretti
        cookie = cookie if cookie is not None else ""
        # Provo login con cookie
        if not self._net_model.login_with_cookie(cookie):
            # Provo login con credenziali
            if not self._net_model.login():
                # Se i login automatici sono falliti mostro login
                self.start()
            else:
                print("Logged con credenziali")
        else:
            print("Logged con cookie")
            if self._main_controller is not None:
                self._main_controller.start()

    def stop(self):
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
            self._main_controller.start()
