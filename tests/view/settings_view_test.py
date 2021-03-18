import os
import sys
import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from src import settings
from src.model.widgets.settings_model import SettingsModel
from src.controllers.settings_controller import SettingsController
from src.view.settings_widget import SettingsWidget

app = QApplication(sys.argv)


class SettingsViewTest(unittest.TestCase):
    """ Test the Policy view """

    def setUp(self) -> None:
        """ Create the GUI """

        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.settings_model = SettingsModel()
        self.settings_view = SettingsWidget(self.settings_model)

        self.path_test = self.settings_view.set_path_view
        self.policy_test = self.settings_view.set_policy_view
        self.quota_test = self.settings_view.set_quota_disk_view

        self.path_test.debug = True

        self.set_policy_controller = SettingsController(self.settings_model, self.settings_view)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        """ Test the path widget in the default state """
        self.assertEqual(self.path_test.titolo.text(), "Cartella da sincronizzare")
        self.assertEqual(self.path_test.titolo.accessibleName(), "Subtitle")
        path = ""
        if self.settings_model.get_path() is not None:
            path = self.settings_model.get_path()
        self.assertEqual(self.path_test.path.text(), path)
        self.assertEqual(self.path_test.change_path_button.text(), "Cambia")

        """ Test the policy widget in the default state """
        self.assertEqual(self.policy_test.client.isChecked(), True)
        self.assertEqual(self.policy_test.manual.isChecked(), False)
        self.assertEqual(self.policy_test._titolo.text(),
                         "Seleziona la politica di gestione dei conflitti")
        self.assertEqual(self.policy_test._titolo.accessibleName(), 'Subtitle')
        self.assertEqual(self.policy_test.client.text(), "Client")
        self.assertEqual(self.policy_test.manual.text(), "Manuale")

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

    def test_update_client(self):
        """ Test the state after setting client radio button true """
        self.policy_test.client.click()
        self.assertEqual(self.policy_test.client.isChecked(), True)
        self.assertEqual(self.policy_test.manual.isChecked(), False)

    def test_update_manual(self):
        """ Test the state after setting manual radio button true """
        # QTest.mouseClick(self.policy_test._manual, Qt.LeftButton)
        self.policy_test.manual.click()
        self.assertEqual(self.policy_test.client.isChecked(), False)
        self.assertEqual(self.policy_test.manual.isChecked(), True)

    def test_client_to_manual(self):
        """ Set client to true then manual to true """
        self.policy_test.client.click()
        self.assertEqual(self.policy_test.client.isChecked(), True)
        self.assertEqual(self.policy_test.manual.isChecked(), False)
        self.policy_test.manual.click()
        self.assertEqual(self.policy_test.client.isChecked(), False)
        self.assertEqual(self.policy_test.manual.isChecked(), True)

    def test_manual_to_client(self):
        """ Set manual to true then client to true """
        self.policy_test.manual.click()
        self.assertEqual(self.policy_test.client.isChecked(), False)
        self.assertEqual(self.policy_test.manual.isChecked(), True)
        self.policy_test.client.click()
        self.assertEqual(self.policy_test.client.isChecked(), True)
        self.assertEqual(self.policy_test.manual.isChecked(), False)


if __name__ == "__main__":
    unittest.main()
