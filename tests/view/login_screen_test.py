from unittest.mock import patch

from PySide2.QtCore import QSettings

from src.controllers.login_controller import LoginController
from src.model.main_model import MainModel
from tests import default_code


class LoginScreenTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()

        self.model = MainModel()
        self.env_settings = QSettings()
        self.env_settings.setValue("Credentials/password", None)
        self.env_settings.setValue("Credentials/user", None)
        self.login_controller = LoginController(self.model, None)
        self.login_test = self.login_controller.login_screen

    def tearDown(self) -> None:
        super().tearDown()

    def test_default(self):
        self.assertEqual(self.login_test.get_user(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.get_psw(), "")

    @patch('src.model.network_model.NetworkModel.login', return_value=True)
    def test_login(self, mock_login):
        self.login_test.login_button.click()
        mock_login.assert_called_once()

    def test_login_fail_slot_exists(self):
        self.login_test.Sl_login_fail()

    @patch('src.model.network_model.NetworkModel.is_logged', return_value=True)
    def test_model_changed(self, mock_is_logged):
        self.login_test.Sl_model_changed()
        mock_is_logged.assert_called_once()
