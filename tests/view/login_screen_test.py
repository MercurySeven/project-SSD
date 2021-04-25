from unittest.mock import patch

from src.controllers.login_controller import LoginController
from src.model.main_model import MainModel
from tests import default_code


class LoginScreenTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super().setUp()

        self.model = MainModel()
        self.login_controller = LoginController(self.model, None)
        self.login_test = self.login_controller.login_screen

    def tearDown(self) -> None:
        super().tearDown()

    def test_default(self):
        self.assertEqual(self.login_test.get_user(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.get_psw(), self.login_test.model.get_password())

    @patch('src.model.network_model.NetworkModel.login', return_value=True)
    def test_login(self, mock_login):
        self.login_test.login_button.click()
        mock_login.assert_called_once()
