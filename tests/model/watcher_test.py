import os
import unittest

from src import settings
from src.model.watcher import Watcher


class WatcherTest(unittest.TestCase):

    def setUp(self) -> None:
        self.test_watcher = Watcher()
        settings.file_name = "tests/config.ini"
        settings.check_file()

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)
