from PySide6.QtCore import Slot

from src.model.network_model import NetworkModel
from src.view.login_screen import LoginScreen


class LoginController:

    def start(self):
        self.login_screen.show()

    def __init__(self, net_model: NetworkModel, main_controller):
        self._net_model = net_model
        self.login_screen = LoginScreen(self._net_model)
        self._main_controller = main_controller

        # Connetto login vista ai due slot del controller
        self.login_screen.Sg_login_success.connect(self.Sl_logged_in)
        self.login_screen.login_button.clicked.connect(self.Sl_login)

        self._net_model.Sg_model_changed.connect(self.login_screen.Sl_model_changed)
        self.login_screen.login_button.click()
        if not self._net_model.login():
            self.start()

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
        self._main_controller.start()
