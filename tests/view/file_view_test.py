import os
import pathlib
import unittest
from unittest.mock import patch

from PySide6.QtCore import QSettings, QCoreApplication

from src import settings
from src.controllers.file_controller import FileController
from src.model.file_model import FileModel
from src.view.file_view import FileView


class FileViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.env_settings = QSettings()
        QCoreApplication.setOrganizationName("MercurySeven")
        QCoreApplication.setApplicationName("SSD")
        self.path = str(pathlib.Path().absolute()) + "/tests"
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        self.env_settings.setValue("sync_path", self.path)
        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.file_model = FileModel()
        self.file_view_test = FileView(self.file_model)
        self.file_controller = FileController(self.file_model, self.file_view_test)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

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
