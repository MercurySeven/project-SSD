import unittest
from unittest.mock import patch

from PySide6.QtCore import QSettings

from src.view.notification_view import NotificationView


class NotificationViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.env_settings = QSettings()
        self.env_settings.setValue("sync_path", "tests")
        self.notify_test = NotificationView()

    def test_defaults(self):
        """ Test notification view test default values"""
        self.assertEqual(self.notify_test.isVisible(), True)
        self.assertEqual(self.notify_test.toolTip(), "Zextras Drive Desktop")
        self.assertEqual(self.notify_test.show_option.text(), "Mostra")
        self.assertEqual(self.notify_test.show_option.toolTip(), "Mostra")
        self.assertEqual(self.notify_test.exit_option.text(), "Esci")
        self.assertEqual(self.notify_test.exit_option.toolTip(), "Esci")

    @patch("PySide6.QtWidgets.QSystemTrayIcon.showMessage")
    def test_show_message_without_duration(self, mock_dialog):
        """ Test if show message gets called, patches the
        default method for the show message in the pyside lib
         so nothing will popup but we'll know that the
         application succeeded in calling the message library"""
        self.notify_test.show_message("ciao", "mamma")
        mock_dialog.assert_called_once()

    @patch("PySide6.QtWidgets.QSystemTrayIcon.showMessage")
    def test_show_message_with_duration(self, mock_dialog):
        """ Test if show message gets called, patches the
        default method for the show message in the pyside lib
         so nothing will popup but we'll know that the
         application succeeded in calling the message library"""
        self.notify_test.show_message("ciao", "mamma", 400000)
        mock_dialog.assert_called_once()
