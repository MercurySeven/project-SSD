from src.controllers.file_controller import FileController
from src.model.main_model import MainModel
from src.view.file_view import FileView
from src.view.widgets.local_file_widget import LocalFileWidget
from src.model.file_model import LocalFile
from tests import default_code
from unittest.mock import patch


class testObject():

    def __init__(self):
        self.st_size = 100


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

    def test_update_files_with_new_path_exists(self):
        self.file_view_test.Sl_update_files_with_new_path("path")

    @patch("os.path.samefile", return_value=True)
    @patch("os.stat", return_value=testObject())
    def test_toggle_files_update(self, mock_os, mock_samefile):
        test_local_file = LocalFile(default_code._get_file_test_node())
        test_local_file_widget = LocalFileWidget(test_local_file)
        self.file_view_test.layout().addWidget(test_local_file_widget)
        self.file_view_test.toggle_files_update("test")
        mock_os.assert_called_once()