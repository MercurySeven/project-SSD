import pathlib
import unittest
import os

from PySide6.QtCore import QSettings

import src.settings as settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.env_settings = QSettings()
        pathlib.Path(str(pathlib.Path().absolute()) + "/tests").mkdir(parents=True, exist_ok=True)
        self.env_settings.setValue("sync_path", str(pathlib.Path().absolute()) + "/tests")
        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_get_quota_disco(self) -> None:
        quota_disco = settings.get_quota_disco()
        self.assertEqual(quota_disco, 1024)

    def test_get_config(self) -> None:
        result = settings.get_config("General", "quota")
        self.assertEqual(result, "1024")

        result = settings.get_config("Generale", "quota")
        self.assertIsNone(result)

        result = settings.get_config("General", "port")
        self.assertIsNone(result)

    def test_update_quota_disco(self) -> None:
        settings.update_quota_disco("1234567")
        self.assertEqual(settings.get_quota_disco(), 1234567)

        settings.update_quota_disco("1000")
        self.assertEqual(settings.get_quota_disco(), 1000)

    def test_get_quota_disco_fix(self) -> None:
        settings.update_quota_disco("ABCDEFG")
        self.assertEqual(settings.get_quota_disco(), 1024)

    def test_update_config(self) -> None:
        settings.update_config("Extra", "darkmode", "True")
        feature = settings.get_config("Extra", "darkmode")
        self.assertEqual(feature, "True")

    def test_update_policy(self) -> None:
        settings.update_policy(2)
        value = settings.get_policy()
        self.assertEqual(value, 2)

    def test_get_policy(self) -> None:
        value = settings.get_policy()
        self.assertEqual(value, 1)

    def test_get_policy_fix(self) -> None:
        settings.update_config("General", "policy", "ABCDE")
        self.assertEqual(settings.get_policy(), 1)

    def test_is_sync(self) -> None:
        value = settings.get_is_synch()
        self.assertFalse(value)

    def test_update_is_sync(self) -> None:
        settings.update_is_sync(True)
        value = settings.get_is_synch()
        self.assertTrue(value)

        settings.update_is_sync(False)
        value = settings.get_is_synch()
        self.assertFalse(value)


if __name__ == "__main__":
    unittest.main()
