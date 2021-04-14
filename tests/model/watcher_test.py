import unittest
from unittest.mock import patch

from src.model.watcher import Watcher
from tests.default_code import setUp, tearDown


class WatcherTest(unittest.TestCase):

    def setUp(self) -> None:
        tmp = setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.restore_credentials = tmp[2]
        self.watcher_to_test = Watcher()

    def tearDown(self) -> None:
        tearDown(self.env_settings, self.restore_path, self.restore_credentials)

    def test_path_change(self):
        string_to_test = "ciao"
        self.assertEqual(self.watcher_to_test.path(), self.env_settings.value("sync_path"))
        self.env_settings.setValue("sync_path", string_to_test)
        self.assertEqual(self.watcher_to_test.path(), string_to_test)

    @patch('src.model.watcher.Watcher.run')
    def test_run_on(self, mock_run):
        self.watcher_to_test.run(True)
        mock_run.assert_called_once()

    @patch('watchdog.observers.api.BaseObserver.unschedule_all')
    @patch('watchdog.observers.api.BaseObserver.stop')
    def test_run_off(self, mock_1, mock_2):
        self.assertEqual(self.watcher_to_test.run(False), True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    def test_background_path_None(self):
        self.env_settings.setValue("sync_path", None)
        self.assertEqual(self.watcher_to_test.background(), False)

    @patch('watchdog.observers.api.BaseObserver.schedule')
    @patch('watchdog.observers.api.BaseObserver.start')
    def test_background_path_not_none(self, mock_1, mock_2):
        self.assertEqual(self.watcher_to_test.background(), True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.model.watcher.Watcher.run')
    def test_reboot(self, mock_run):
        self.watcher_to_test.reboot()
        self.assertEqual(mock_run.call_count, 2)
