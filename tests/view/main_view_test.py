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

    def test_switch_view_to_files(self):
        self.main_widget_test.chage_current_view_to_files()
        self.assertEqual(self.main_widget_test.settings_button.isChecked(), False)
        self.assertEqual(self.main_widget_test.remote_button.isChecked(), False)
        self.assertEqual(self.main_widget_test.files_button.isChecked(), True)
        self.assertEqual(
            self.main_widget_test.swidget.currentWidget(),
            self.main_widget_test.files_widget)

    def test_switch_view_to_remote(self):
        self.main_widget_test.chage_current_view_to_remote()
        self.assertEqual(self.main_widget_test.settings_button.isChecked(), False)
        self.assertEqual(self.main_widget_test.remote_button.isChecked(), True)
        self.assertEqual(self.main_widget_test.files_button.isChecked(), False)
        self.assertEqual(
            self.main_widget_test.swidget.currentWidget(),
            self.main_widget_test.remote_widget)

    def test_switch_view_to_settings(self):
        self.main_widget_test.chage_current_view_to_settings()
        self.assertEqual(self.main_widget_test.settings_button.isChecked(), True)
        self.assertEqual(self.main_widget_test.remote_button.isChecked(), False)
        self.assertEqual(self.main_widget_test.files_button.isChecked(), False)
        self.assertEqual(
            self.main_widget_test.swidget.currentWidget(),
            self.main_widget_test.settings_view)

    def test_remote_button(self):
        self.main_widget_test.remote_button.click()
        self.assertEqual(self.main_widget_test.remote_button.isChecked(), True)

    def test_files_button(self):
        self.main_widget_test.files_button.setChecked(False)
        self.main_widget_test.files_button.click()
        self.assertEqual(self.main_widget_test.files_button.isChecked(), True)

    def test_settings_button(self):
        self.main_widget_test.settings_button.click()
        self.assertEqual(self.main_widget_test.settings_button.isChecked(), True)
