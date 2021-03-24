import unittest
from src import settings
from src.model.main_model import MainModel
from src.view.login_screen import LoginScreen


class LoginScreenTest(unittest.TestCase):
    def setUp(self) -> None:
        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.model = MainModel()
        self.login_test = LoginScreen(self.model.network_model)

    def test_default(self):
        self.assertEqual(self.login_test.userField.text(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.pswField.text(), self.login_test.model.get_password())
