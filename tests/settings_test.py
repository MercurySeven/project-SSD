import unittest
import os

import src.settings as settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
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


if __name__ == "__main__":
    unittest.main()
