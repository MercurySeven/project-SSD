import os
import unittest
import sys
# Serve perchè sennò non puoi avere widget
from PySide6.QtWidgets import QApplication, QWidget

from src import settings
from src.view.widgets.settings.set_policy_view import SetPolicyView
from src.model.widgets.settings_model import SettingsModel
from src.controllers.widgets.settings.set_policy_controller import SetPolicyController

app = QApplication(sys.argv)


class SetPolicyViewTest(unittest.TestCase):
    """ Test the Policy view """

    def setUp(self) -> None:
        """ Create the GUI """

        settings.file_name = "tests/config.ini"
        settings.create_standard_settings()
        self.settings_model = SettingsModel()
        self.set_policy_controller = SetPolicyController(self.settings_model)
        self.widget = QWidget()
        self.policy_test = SetPolicyView(
            self.settings_model,
            self.set_policy_controller,
            self.widget)

    def tearDown(self) -> None:
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    def test_defaults(self):
        """ Test the widget in the default state """
        self.assertEqual(self.policy_test._client.isChecked(), True)
        self.assertEqual(self.policy_test._manual.isChecked(), False)

    def test_update_client(self):
        """ Test the state after setting client radio button true """
        self.policy_test._client.click()
        self.assertEqual(self.policy_test._client.isChecked(), True)
        self.assertEqual(self.policy_test._manual.isChecked(), False)

    def test_update_manual(self):
        """ Test the state after setting manual radio button true """
        # QTest.mouseClick(self.policy_test._manual, Qt.LeftButton)
        self.policy_test._manual.click()
        self.assertEqual(self.policy_test._client.isChecked(), False)
        self.assertEqual(self.policy_test._manual.isChecked(), True)

    def test_client_to_manual(self):
        """ Set client to true then manual to true """
        self.policy_test._client.click()
        self.assertEqual(self.policy_test._client.isChecked(), True)
        self.assertEqual(self.policy_test._manual.isChecked(), False)
        self.policy_test._manual.click()
        self.assertEqual(self.policy_test._client.isChecked(), False)
        self.assertEqual(self.policy_test._manual.isChecked(), True)


if __name__ == "__main__":
    unittest.main()
