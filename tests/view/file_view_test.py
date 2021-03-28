import os
import pathlib
import unittest
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication, QSettings

from src import settings
from src.controllers.file_controller import FileController
from src.model.main_model import MainModel
from src.view.file_view import FileView


class FileViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.env_settings = QSettings()
        QCoreApplication.setOrganizationName("MercurySeven")
        QCoreApplication.setApplicationName("SSD")
        self.restore_path = self.env_settings.value("sync_path")

        self.path = os.path.join(str(pathlib.Path().absolute()), "tests")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        settings.file_name = os.path.join(self.path, "config.ini")

        print("AAAAAAAAAAAAAAAAAAAAAAAAa" + self.path)

        self.env_settings.setValue("sync_path", self.path)

        print("BBBBBBBBBBBBBBBBBBBBBBB " + self.env_settings.value("sync_path"))
        settings.create_standard_settings()

        self.main_model = MainModel()
        self.file_view_test = FileView(self.main_model.file_model)
        self.file_controller = FileController(self.main_model.file_model, self.file_view_test)

    def tearDown(self) -> None:
        os.remove(settings.file_name)
        # self.env_settings.setValue("sync_path", self.restore_path)

    def test_defaults(self):
        """ Test file view test default values"""
        self.assertEqual(self.file_view_test.title.text(), "File sincronizzati")
        self.assertEqual(self.file_view_test.title.accessibleName(), "Title")

        self.assertEqual(self.file_view_test.show_path_button.text(), "Apri file manager")

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_show_path_button(self, mock_dialog):
        """ Test if show path button calls the right method and execute
        Correctly"""
        self.file_view_test.show_path_button.click()
        mock_dialog.assert_called_once()
