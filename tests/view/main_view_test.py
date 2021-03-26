import os
import unittest

from PySide6.QtCore import QSettings

from src import settings
from src.model.main_model import MainModel
from src.view.main_view import MainWindow, MainWidget


class MainWindowTest(unittest.TestCase):

    def setUp(self) -> None:
        self.env_settings = QSettings()
        self.env_settings.setValue("sync_path", "tests")
        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.main_model = MainModel()
        self.main_window = MainWindow(self.main_model)
        self.main_widget_test = self.main_window.main_widget
        self.main_widget_double = MainWidget(self.main_model)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        self.assertEqual(self.main_widget_test.container_menu.accessibleName(),
                         self.main_widget_double.container_menu.accessibleName())
        self.assertEqual(self.main_widget_test.files_button.isChecked(),
                         self.main_widget_double.files_button.isChecked())
        self.assertEqual(self.main_widget_test.swidget.accessibleName(),
                         self.main_widget_double.swidget.accessibleName())