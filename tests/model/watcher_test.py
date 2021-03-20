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

    def test_run_on(self):
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)

    def test_run_off(self):
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)

    def test_run_on_off(self):
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)

    def test_run_on_off_off(self):
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)

    def test_run_off_on_on(self):
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)

    def test_run_on_on(self):
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)
        self.test_watcher.run(True)
        self.assertEqual(self.test_watcher.is_running, True)

    def test_run_off_off(self):
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)
        self.test_watcher.run(False)
        self.assertEqual(self.test_watcher.is_running, False)
