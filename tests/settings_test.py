import unittest
import os

from src import settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        settings.create_standard_settings()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_get_server_url(self) -> None:
        url = settings.get_server_url()
        self.assertEqual(url, "http://20.56.176.12:80/")

    def test_get_server_url_with_slash(self) -> None:
        settings.update_config(
            "Connection", "address", "http://20.56.176.12/")
        url = settings.get_server_url()
        self.assertEqual(url, "http://20.56.176.12:80/")

    def test_get_quota_disco(self) -> None:
        quota_disco = settings.get_quota_disco()
        self.assertEqual(quota_disco, 1024)

    def test_get_config(self) -> None:
        result = settings.get_config("Connection", "port")
        self.assertEqual(result, "80")

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
        settings.update_config("Connection", "port", "22")
        url = settings.get_server_url()
        self.assertEqual(url, "http://20.56.176.12:22/")

        settings.update_config("Connection", "proxy", "3500")
        proxy = settings.get_config("Connection", "proxy")
        self.assertEqual(proxy, "3500")

        settings.update_config("Extra", "darkmode", "True")
        feature = settings.get_config("Extra", "darkmode")
        self.assertEqual(feature, "True")


if __name__ == "__main__":
    unittest.main()
