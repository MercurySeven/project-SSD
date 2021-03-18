import os
import unittest
from PySide6.QtWidgets import QWidget
from unittest.mock import patch

from src import settings
from src.view.widgets.settings.set_path_view import SetPathView
from src.model.widgets.settings_model import SettingsModel
from src.controllers.widgets.settings.set_path_controller import SetPathController


class SetPolicyViewTest(unittest.TestCase):
    """ Test the Policy view """

    def setUp(self) -> None:
        """ Create the GUI """

        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.settings_model = SettingsModel()
        self.widget = QWidget()
        self.path_test = SetPathView(self.settings_model, True)
        self.set_policy_controller = SetPathController(self.settings_model, self.path_test)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        """ Test the widget in the default state """
        self.assertEqual(self.path_test.titolo.text(), "Cartella da sincronizzare")
        self.assertEqual(self.path_test.titolo.accessibleName(), "Subtitle")
        path = ""
        if self.settings_model.get_path() is not None:
            path = self.settings_model.get_path()
        self.assertEqual(self.path_test.path.text(), path)
        self.assertEqual(self.path_test.change_path_button.text(), "Cambia")

    # patch is used to "make and empty shell" of the method passed so we can just check if
    # the methods gets called or not
    @patch("src.view.widgets.settings.set_path_view.SetPathView.Sl_show_file_dialog")
    def test_popup_file_dialog(self, mock_dialog):
        """ Test if popup dialog for choosing files get called once"""
        self.path_test.change_path_button.click()
        mock_dialog.assert_called_once()

    def test_popup_file_dialog_interaction(self):
        self.path_test.path.setText("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.assertEqual(self.path_test.path.text(), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.path_test.change_path_button.click()
        path = ""
        if self.settings_model.get_path() is not None:
            path = self.settings_model.get_path()
        self.assertEqual(self.path_test.path.text(), path)


if __name__ == "__main__":
    unittest.main()
