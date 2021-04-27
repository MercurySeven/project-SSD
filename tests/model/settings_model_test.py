import unittest

import bitmath

from src.model.main_model import MainModel
from src.model.algorithm.policy import Policy
from tests import default_code


class TestSettings(default_code.DefaultCode):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()
        self.main_model = MainModel()
        self.sett_model = self.main_model.settings_model

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()

    def test_get_policy(self) -> None:
        result = self.sett_model.get_policy()
        self.assertEqual(Policy.Client, result)

    def test_set_policy(self) -> None:
        result = self.sett_model.get_policy()
        self.assertEqual(Policy.Client, result)

        self.sett_model.set_policy(Policy.Manual)

        result = self.sett_model.get_policy()
        self.assertEqual(Policy.Manual, result)

    def test_set_sync_time(self) -> None:
        result = self.sett_model.get_sync_time()
        self.assertEqual(15, result)
        new_time = 20
        self.sett_model.set_sync_time(new_time)
        result = self.sett_model.get_sync_time()
        self.assertEqual(new_time, result)

    def test_convert_size(self) -> None:
        test: dict[str, int] = {
            "0 B": 0,
            "1.0 KiB": 1024,
            "2.0 KiB": 2048,
            "1000.0 KiB": 1024000,
            "976.56 MiB": 1024000000
        }

        for key, value in test.items():
            self.assertEqual(key, self.sett_model.convert_size(value))

    def test_get_quota_disco(self) -> None:
        value = self.sett_model.get_quota_disco()
        self.assertEqual("1.0 KiB", value)

    def test_get_quota_disco_raw(self) -> None:
        value = self.sett_model.get_quota_disco_raw()
        self.assertEqual(1024, value)

    def test_set_quota_disco(self) -> None:
        value = self.sett_model.convert_size(self.sett_model.get_quota_disco_raw())
        value = bitmath.parse_string(value).to_Byte()
        self.assertEqual(1024, value)
        new_value = self.sett_model.convert_size(self.sett_model.get_size() + 1)
        new_value = bitmath.parse_string(new_value)
        self.sett_model.set_quota_disco(new_value.to_Byte())

        value = self.sett_model.convert_size(self.sett_model.get_quota_disco_raw())
        self.assertEqual(new_value, bitmath.parse_string(value))

        value = bitmath.parse_string(self.sett_model.get_quota_disco())
        self.assertEqual(new_value, value)


if __name__ == "__main__":
    unittest.main()
