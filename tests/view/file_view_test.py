from src.controllers.file_controller import FileController
from src.model.main_model import MainModel
from src.view.file_view import FileView
from tests import default_code
from unittest.mock import patch


class FileViewTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()

        self.main_model = MainModel()
        self.file_view_test = FileView(self.main_model.file_model)
        self.file_controller = FileController(self.main_model.file_model, self.file_view_test)

    def tearDown(self) -> None:
        super().tearDown()

    def test_defaults(self):
        """ Test file view test default values"""
        self.assertEqual(self.file_view_test.title.text(), "File locali")
        self.assertEqual(self.file_view_test.title.accessibleName(), "Title")
        self.assertEqual(self.file_view_test.show_path_button.text(), "Apri file manager")

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_show_path_button(self, mock_dialog):
        """ Test if show path button calls the right method and execute
        correctly"""
        self.file_view_test.show_path_button.click()
        mock_dialog.assert_called_once()
