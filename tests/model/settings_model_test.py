import unittest
import os

from PySide6.QtCore import QSettings

from src.model.settings_model import SettingsModel
from src.network.policy import Policy
from src import settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.sett_model = SettingsModel()
        self.env_settings = QSettings()
        self.env_settings.setValue("sync_path", "tests")
        settings.file_name = "tests/config.ini"
        settings.check_file()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_get_policy(self) -> None:
        result = self.sett_model.get_policy()
        self.assertEqual(Policy.Client, result)

    def test_set_policy(self) -> None:
        result = self.sett_model.get_policy()
        self.assertEqual(Policy.Client, result)

        self.sett_model.set_policy(Policy.Manual)

        result = self.sett_model.get_policy()
        self.assertEqual(Policy.Manual, result)

    def test_convert_size(self) -> None:
        test: dict[str, int] = {
            "0 B": 0,
            "1.0 KB": 1024,
            "2.0 KB": 2048,
            "1000.0 KB": 1024000,
            "976.56 MB": 1024000000
        }

        for key, value in test.items():
            self.assertEqual(key, self.sett_model.convert_size(value))

    def test_get_quota_disco(self) -> None:
        value = self.sett_model.get_quota_disco()
        self.assertEqual("1.0 KB", value)

    def test_get_quota_disco_raw(self) -> None:
        value = self.sett_model.get_quota_disco_raw()
        self.assertEqual(1024, value)

    def test_set_quota_disco(self) -> None:
        value = self.sett_model.get_quota_disco_raw()
        self.assertEqual(1024, value)

        self.sett_model.set_quota_disco("2048")

        value = self.sett_model.get_quota_disco_raw()
        self.assertEqual(2048, value)

        value = self.sett_model.get_quota_disco()
        self.assertEqual("2.0 KB", value)


if __name__ == "__main__":
    unittest.main()
