import unittest
from unittest.mock import patch
from src.controllers.file_controller import FileController
from src.model.main_model import MainModel
from src.view.file_view import FileView
from tests import default_code


class FileViewTest(unittest.TestCase):

    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]

        self.main_model = MainModel()
        self.file_view_test = FileView(self.main_model.file_model)
        self.file_controller = FileController(self.main_model.file_model, self.file_view_test)

    def tearDown(self) -> None:
        default_code.tearDown(self.env_settings, self.restore_path)

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
