import os
import pathlib
import unittest

from src import settings
from src.model.main_model import MainModel
from src.view.login_screen import LoginScreen


class LoginScreenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path = os.path.join(str(pathlib.Path().absolute()), "tests")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        settings.file_name = os.path.join(self.path, "config.ini")
        settings.create_standard_settings()
        self.model = MainModel()
        self.login_test = LoginScreen(self.model.network_model)

    def tearDown(self) -> None:
        os.remove(settings.file_name)

    def test_default(self):
        self.assertEqual(self.login_test.userField.text(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.pswField.text(), self.login_test.model.get_password())
