import unittest
from src.model.main_model import MainModel
from src.view.main_view import MainWindow, MainWidget
from tests import default_code


class MainWindowTest(unittest.TestCase):

    def setUp(self) -> None:

        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.main_model = MainModel()
        self.main_window = MainWindow(self.main_model)
        self.main_widget_test = self.main_window.main_widget
        self.main_widget_double = MainWidget(self.main_model)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        default_code.tearDown(self.env_settings, self.restore_path)

    def test_defaults(self):
        self.assertEqual(self.main_widget_test.container_menu.accessibleName(),
                         self.main_widget_double.container_menu.accessibleName())
        self.assertEqual(self.main_widget_test.files_button.isChecked(),
                         self.main_widget_double.files_button.isChecked())
        self.assertEqual(self.main_widget_test.swidget.accessibleName(),
                         self.main_widget_double.swidget.accessibleName())
