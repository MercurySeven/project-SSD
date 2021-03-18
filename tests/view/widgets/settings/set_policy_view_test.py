import os
import unittest
import sys
# Serve perchè sennò non puoi avere widget
from PySide6.QtWidgets import QApplication, QWidget

from src import settings
from src.view.widgets.settings.set_policy_view import SetPolicyView
from src.controllers.settings_controller import SettingsController
from src.view.settings_widget import SettingsWidget
from src.model.widgets.settings_model import SettingsModel
app = QApplication(sys.argv)


class SetPolicyViewTest(unittest.TestCase):
    """ Test the Policy view """

    def setUp(self) -> None:
        """ Create the GUI """

        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.settings_model = SettingsModel()

        self.settings_view = SettingsWidget(self.settings_model)
        self.policy_test = self.settings_view.set_policy_view
        self.settings_controller = SettingsController(self.settings_model, self.settings_view)


    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        """ Test the widget in the default state """
        self.assertEqual(self.policy_test.client.isChecked(), True)
        self.assertEqual(self.policy_test.manual.isChecked(), False)
        self.assertEqual(self.policy_test._titolo.text(),
                         "Seleziona la politica di gestione dei conflitti")
        self.assertEqual(self.policy_test._titolo.accessibleName(), 'Subtitle')
        self.assertEqual(self.policy_test.client.text(), "Client")
        self.assertEqual(self.policy_test.manual.text(), "Manuale")

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
