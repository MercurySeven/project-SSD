import os
import unittest
from PySide6.QtWidgets import QWidget

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
        self.set_policy_controller = SetPathController(self.settings_model)
        self.widget = QWidget()
        self.path_test = SetPathView(
            self.settings_model,
            self.set_policy_controller,
            self.widget)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        """ Test the widget in the default state """
        self.assertEqual(self.path_test.titolo.text(), "Cartella da sincronizzare")
        self.assertEqual(self.path_test.titolo.accessibleName(), "Subtitle")
        self.assertEqual(self.path_test.path.text(), self.settings_model.get_path())
        self.assertEqual(self.path_test.change_path_button.text(), "Cambia")


if __name__ == "__main__":
    unittest.main()
