import unittest
import os
from settings import Settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.settings = Settings(os.path.join("tests", "config.ini"))
        self.settings.create_standard_settings()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(self.settings.file_name)

    def test_get_server_url(self) -> None:
        url = self.settings.get_server_url()
        self.assertEqual(url, "http://20.56.176.12:80/")

    def test_get_server_url_with_slash(self) -> None:
        self.settings.update_config(
            "Connection", "address", "http://20.56.176.12/")
        url = self.settings.get_server_url()
        self.assertEqual(url, "http://20.56.176.12:80/")

    def test_get_quota_disco(self) -> None:
        quota_disco = self.settings.get_quota_disco()
        self.assertEqual(quota_disco, 1024)

    def test_get_config(self) -> None:
        result = self.settings.get_config("Connection", "port")
        self.assertEqual(result, "80")

        result = self.settings.get_config("Generale", "quota")
        self.assertIsNone(result)

        result = self.settings.get_config("General", "port")
        self.assertIsNone(result)

    def test_update_quota_disco(self) -> None:
        self.settings.update_quota_disco("1234567")
        self.assertEqual(self.settings.get_quota_disco(), 1234567)

        self.settings.update_quota_disco("1000")
        self.assertEqual(self.settings.get_quota_disco(), 1000)

    def test_get_quota_disco_fix(self) -> None:
        self.settings.update_quota_disco("ABCDEFG")
        self.assertEqual(self.settings.get_quota_disco(), 1024)

    def test_update_config(self) -> None:
        self.settings.update_config("Connection", "port", "22")
        url = self.settings.get_server_url()
        self.assertEqual(url, "http://20.56.176.12:22/")

        self.settings.update_config("Connection", "proxy", "3500")
        proxy = self.settings.get_config("Connection", "proxy")
        self.assertEqual(proxy, "3500")

        self.settings.update_config("Extra", "darkmode", "True")
        feature = self.settings.get_config("Extra", "darkmode")
        self.assertEqual(feature, "True")

    def test_file_already_exists(self) -> None:
        local_settings = Settings(os.path.join("tests", "config.ini"))
        quota_disco = local_settings.get_quota_disco()
        self.assertEqual(quota_disco, 1024)

        local_settings.update_quota_disco("123456")

        quota_disco = self.settings.get_quota_disco()
        self.assertEqual(quota_disco, 123456)


if __name__ == "__main__":
    unittest.main()
