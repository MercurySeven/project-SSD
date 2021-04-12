import unittest

from src.model.settings_model import SettingsModel
from src.model.algorithm.policy import Policy
from tests import default_code


class TestSettings(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]

        self.sett_model = SettingsModel()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        default_code.tearDown(self.env_settings, self.restore_path)

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
        new_value = self.sett_model.get_size() + 1
        self.sett_model.set_quota_disco(str(new_value))

        value = self.sett_model.get_quota_disco_raw()
        self.assertEqual(new_value, value)

        value = self.sett_model.get_quota_disco()
        self.assertEqual(self.sett_model.convert_size(new_value), value)


if __name__ == "__main__":
    unittest.main()
