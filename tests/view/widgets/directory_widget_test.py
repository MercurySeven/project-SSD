import unittest

from tests import default_code


class DirectoryWidgetTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.restore_credentials = tmp[2]

    def tearDown(self) -> None:
        default_code.tearDown(self.env_settings, self.restore_path, self.restore_credentials)
