from PySide6.QtCore import Slot

from src.network.api import Api
from src.view.login_screen import LoginScreen


class LoginController:

    def __init__(self, net_model: Api, next_controller):
        self._net_model = net_model
        self.login_screen = LoginScreen(self._net_model)
        self.login_screen.show()
        self._next_controller = next_controller

        # Connetto login vista ai due slot del controller
        self.login_screen.Sg_login_success.connect(self.Sl_logged_in)
        self.login_screen.login_button.clicked.connect(self.Sl_login)

        self._net_model.Sg_model_changed.connect(self.login_screen.Sl_model_changed)

    @Slot()
    def Sl_login(self):
        user = self.login_screen.get_user()
        pwd = self.login_screen.get_psw()
        self._net_model.login(user, pwd)

    @Slot()
    def Sl_logged_in(self):
        self.login_screen.hide()
        self.login_screen.close()
        self._next_controller.start()
