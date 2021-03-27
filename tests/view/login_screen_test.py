import pathlib
import unittest

from PySide6.QtCore import QSettings

from src import settings
from src.model.main_model import MainModel
from src.view.login_screen import LoginScreen


class LoginScreenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env_settings = QSettings()
        pathlib.Path(str(pathlib.Path().absolute()) + "/tests").mkdir(parents=True, exist_ok=True)
        self.env_settings.setValue("sync_path", str(pathlib.Path().absolute()) + "/tests")
        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.model = MainModel()
        self.login_test = LoginScreen(self.model.network_model)

    def test_default(self):
        self.assertEqual(self.login_test.userField.text(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.pswField.text(), self.login_test.model.get_password())
