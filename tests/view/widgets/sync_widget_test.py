import os
import unittest

from PySide6.QtCore import QSize, QSettings

from src import settings
from src.model.widgets.sync_model import SyncModel
from src.view.widgets.sync_widget import SyncWidget
from src.controllers.widgets.sync_controller import SyncController


class SyncWidgetTest(unittest.TestCase):
    """ Test synchronized widget class"""

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.env_settings = QSettings()
        self.env_settings.setValue("sync_path", "tests")
        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.sync_model = SyncModel()
        self.test_sync = SyncWidget(self.sync_model)
        self.controller = SyncController(self.sync_model, self.test_sync)

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        """Test default synchronized widget"""
        self.assertEqual(self.test_sync.watch_label.text(), "SYNC")
        self.assertEqual(self.test_sync.watch_label.accessibleName(), "Title")

        self.assertEqual(self.test_sync.running_label.text(), "Disattivata")
        self.assertEqual(self.test_sync.running_label.accessibleName(), "Subtitle")

        self.assertEqual(self.test_sync.syncButton.iconSize(), QSize(50, 50))
        self.assertEqual(self.test_sync.syncButton.isCheckable(), True)
        self.assertEqual(self.test_sync.syncButton.accessibleName(), "HighlightButton")

        self.assertEqual(self.test_sync.menu_label.text(), "• • •")

    def test_turn_on_sync(self):
        self.test_sync.syncButton.click()
        self.assertEqual(self.test_sync.syncButton.isChecked(), self.test_sync._model.get_state())
        self.assertEqual(self.test_sync.running_label.text(), "Attivata")

    def test_turn_off_sync(self):
        self.test_sync.syncButton.click()
        self.assertEqual(self.test_sync.syncButton.isChecked(), self.test_sync._model.get_state())
        self.assertEqual(self.test_sync.running_label.text(), "Attivata")
        self.test_sync.syncButton.click()
        self.assertEqual(self.test_sync.syncButton.isChecked(), self.test_sync._model.get_state())
        self.assertEqual(self.test_sync.running_label.text(), "Disattivata")


if __name__ == "__main__":
    unittest.main()
