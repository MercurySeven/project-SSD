import unittest
from unittest.mock import patch

from src.model.main_model import MainModel
from src.controllers.settings_controller import SettingsController
from src.view.settings_view import SettingsView
from tests import default_code


class SettingsViewTest(default_code.DefaultCode):
    """ Test the Policy view """

    def setUp(self) -> None:
        """ setup for settings view"""
        super().setUp()

        self.main_model = MainModel()
        self.settings_view = SettingsView(self.main_model)

        self.path_test = self.settings_view.set_path_widget
        self.policy_test = self.settings_view.set_policy_widget
        self.quota_test = self.settings_view.set_quota_disk_widget

        self.path_test.debug = True

        self.set_policy_controller = SettingsController(self.main_model, self.settings_view)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()

    def test_defaults(self):
        """ Test the path widget in the default state """
        self.assertEqual(self.path_test.titolo.text(), "Cartella sincronizzata")
        self.assertEqual(self.path_test.titolo.accessibleName(), "Title2")
        path = ""
        if self.main_model.settings_model.get_path() is not None:
            path = self.main_model.settings_model.get_path()
        self.assertEqual(self.path_test.path.text(), path)
        self.assertEqual(self.path_test.change_path_button.text(), "Cambia")

        """ Test the policy widget in the default state """
        self.assertTrue(self.policy_test.client.isChecked())
        self.assertFalse(self.policy_test.manual.isChecked())
        self.assertEqual(self.policy_test.titolo.text(), "Politica di gestione conflitti")
        self.assertEqual(self.policy_test.titolo.accessibleName(), 'Title2')
        self.assertEqual("Client" in self.policy_test.client.text(), True)
        self.assertEqual("Manuale" in self.policy_test.manual.text(), True)

        """ Test the quota disk widget in the default state """
        self.assertEqual(self.quota_test.accessibleName(), "InfoBox")
        self.assertEqual(self.quota_test.title.text(), "Spazio di archiviazione")
        self.assertEqual(self.quota_test.title.accessibleName(), "Title2")
        self.assertEqual(self.quota_test.progress_label.text(), "Spazio occupato:")
        self.assertEqual(self.quota_test.progress_label.accessibleName(), "")

    # patch is used to "make and empty shell" of the method passed so we can just check if
    # the methods gets called or not

    @patch("src.view.widgets.settings.set_path_widget.SetPathWidget.Sl_show_file_dialog")
    def test_popup_file_dialog(self, mock_dialog):
        """ Test if popup dialog for choosing files get called once"""
        self.path_test.change_path_button.click()
        mock_dialog.assert_called_once()

    @patch("PySide6.QtWidgets.QDialog.exec")
    def test_popup_file_dialog_interaction(self, mock_dialog):
        self.path_test.path.setText("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.assertEqual(self.path_test.path.text(), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.path_test.change_path_button.click()
        path = ""
        if self.main_model.settings_model.get_path() is not None:
            path = self.main_model.settings_model.get_path()
        self.assertEqual(self.path_test.path.text(), path)
        mock_dialog.assert_called_once()

    def test_update_client(self):
        """ Test the state after setting client radio button true """
        self.policy_test.client.click()
        self.assertTrue(self.policy_test.client.isChecked())
        self.assertFalse(self.policy_test.manual.isChecked())

    def test_update_manual(self):
        """ Test the state after setting manual radio button true """
        # QTest.mouseClick(self.policy_test._manual, Qt.LeftButton)
        self.policy_test.manual.click()
        self.assertFalse(self.policy_test.client.isChecked())
        self.assertTrue(self.policy_test.manual.isChecked())

    def test_client_to_manual(self):
        """ Set client to true then manual to true """
        self.policy_test.client.click()
        self.assertTrue(self.policy_test.client.isChecked())
        self.assertFalse(self.policy_test.manual.isChecked())
        self.policy_test.manual.click()
        self.assertFalse(self.policy_test.client.isChecked())
        self.assertTrue(self.policy_test.manual.isChecked())

    def test_manual_to_client(self):
        """ Set manual to true then client to true """
        self.policy_test.manual.click()
        self.assertFalse(self.policy_test.client.isChecked())
        self.assertTrue(self.policy_test.manual.isChecked())
        self.policy_test.client.click()
        self.assertTrue(self.policy_test.client.isChecked())
        self.assertFalse(self.policy_test.manual.isChecked())

    def test_quota_change(self):
        """ Test changing the quota"""
        self.quota_test.dedicated_space.setText("2222")
        self.quota_test.Sl_dedicated_space_changed()
        value = self.main_model.settings_model.convert_size(
            self.main_model.settings_model.get_size())
        new_max_quota = self.main_model.settings_model.get_quota_disco()
        self.assertEqual(self.quota_test.disk_quota.text(), f"{value} su {new_max_quota} in uso")


if __name__ == "__main__":
    unittest.main()
