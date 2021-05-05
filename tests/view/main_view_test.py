from unittest.mock import patch
from src.model.main_model import MainModel
from src.view.main_view import MainWindow, MainWidget
from tests import default_code


class MainWindowTest(default_code.DefaultCode):
    @patch('src.view.remote_file_view.RemoteFileView.Sl_model_changed')
    def setUp(self, mock_1) -> None:

        super().setUp()
        self.main_model = MainModel()
        self.main_window = MainWindow(self.main_model)
        self.main_widget_test = self.main_window.main_widget
        self.main_widget_double = MainWidget(self.main_model)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()

    def test_defaults(self):
        self.assertEqual(self.main_widget_test.container_menu.accessibleName(),
                         self.main_widget_double.container_menu.accessibleName())
        self.assertEqual(self.main_widget_test.files_button.isChecked(),
                         self.main_widget_double.files_button.isChecked())
        self.assertEqual(self.main_widget_test.swidget.accessibleName(),
                         self.main_widget_double.swidget.accessibleName())
