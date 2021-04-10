import unittest
from src.model.main_model import MainModel
from src.view.login_screen import LoginScreen
from tests import default_code


class LoginScreenTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]

        self.model = MainModel()
        self.login_test = LoginScreen(self.model.network_model)

    def tearDown(self) -> None:
        default_code.tearDown(self.env_settings, self.restore_path)

    def test_default(self):
        self.assertEqual(self.login_test.get_user(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.get_psw(), self.login_test.model.get_password())
