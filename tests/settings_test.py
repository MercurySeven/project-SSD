
import unittest

import src.settings as settings
from tests import default_code


class TestSettings(default_code.DefaultCode):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()

    def test_get_quota_disco(self) -> None:
        quota_disco = settings.get_quota_disco()
        self.assertEqual(quota_disco, 20971520.0)

    def test_get_config(self) -> None:
        result = settings.get_config("General", "quota")
        self.assertEqual(result, "20971520.0")

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
