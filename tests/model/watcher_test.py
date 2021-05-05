import os
import pathlib
import time
from unittest.mock import patch

from src.model.watcher import Watcher
from tests import default_code


class WatcherTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()
        self.env_settings = super().get_env_settings()
        self.watcher_to_test = Watcher()
        self.path = self.env_settings.value(super().SYNC_ENV_VARIABLE)
        self.path = os.path.join(self.path, "folder")
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        self.file_test = os.path.join(self.path, "test.txt")

    def delete_files(self):
        if os.path.exists(self.file_test):
            try:
                os.remove(self.file_test)
            except Exception as e:
                print(e)
        if os.path.exists(self.file_test + "aa"):
            try:
                os.remove(self.file_test + "aa")
            except Exception as e:
                print(e)
        if os.path.exists(self.path):
            try:
                os.rmdir(self.path)
            except Exception as e:
                print(e)

    def tearDown(self) -> None:
        self.delete_files()
        super().tearDown()

    def test_path_change(self):
        string_to_test = "ciao"
        self.assertEqual(self.watcher_to_test.path(), self.env_settings.value("sync_path"))
        self.env_settings.setValue("sync_path", string_to_test)
        self.assertEqual(self.watcher_to_test.path(), string_to_test)

    @patch('src.model.watcher.Watcher.background')
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

    @patch('src.model.watcher.MyHandler.signal_watchdog')
    def test_handler_create(self, mock_1):
        self.env_settings.setValue("sync_path", self.path)
        self.watcher_to_test.reboot()
        with open(self.file_test, "w"):
            pass
        time.sleep(0.5)
        counter = mock_1.call_count
        self.assertEqual(counter > 0, True)

    @patch('src.model.watcher.MyHandler.signal_watchdog')
    def test_handler_delete(self, mock_1):
        self.env_settings.setValue("sync_path", self.path)
        with open(self.file_test, "w"):
            pass
        self.watcher_to_test.reboot()
        os.remove(self.file_test)
        time.sleep(0.5)
        counter = mock_1.call_count
        self.assertEqual(counter > 0, True)

    @patch('src.model.watcher.MyHandler.signal_watchdog')
    def test_handler_moved(self, mock_1):
        self.env_settings.setValue("sync_path", self.path)
        with open(self.file_test, "w"):
            pass
        self.watcher_to_test.reboot()
        os.rename(self.file_test, self.file_test + "aa")
        time.sleep(0.5)
        counter = mock_1.call_count
        self.assertEqual(counter > 0, True)
