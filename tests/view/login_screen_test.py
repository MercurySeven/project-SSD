import os
import pathlib
import unittest

from PySide6.QtCore import QSettings, QCoreApplication

from src import settings
from src.model.main_model import MainModel
from src.view.login_screen import LoginScreen


class LoginScreenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env_settings = QSettings()
        QCoreApplication.setOrganizationName("MercurySeven")
        QCoreApplication.setApplicationName("SSD")
        self.restore_path = self.env_settings.value("sync_path")

        self.path = os.path.join(str(pathlib.Path().absolute()), "tests")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        settings.file_name = os.path.join(self.path, "config.ini")

        self.env_settings.setValue("sync_path", self.path)

        settings.create_standard_settings()
        self.model = MainModel()
        self.login_test = LoginScreen(self.model.network_model)

    def tearDown(self) -> None:
        os.remove(settings.file_name)
        self.env_settings.setValue("sync_path", self.restore_path)

    def test_default(self):
        self.assertEqual(self.login_test.userField.text(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.pswField.text(), self.login_test.model.get_password())
