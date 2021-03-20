import unittest

from src.model.file import File
from src.view.widgets.filewidget import FileWidget
from unittest.mock import patch


class FileWidgetTest(unittest.TestCase):

    def setUp(self) -> None:
        self.file = File("nome", "creation date", "last mod date", "txt", "100", "status")
        self.file_view_test = FileWidget(self.file)

    def test_defaults(self):
        """ Test file_widget default values"""
        to_compare = "Ultima modifica: " + self.file.get_last_modified_date() + "\nSize: " + \
            self.file.get_size()
        self.assertEqual(self.file_view_test.accessibleName(), "File")
        self.assertEqual(self.file_view_test.toolTip(), to_compare)
        self.assertEqual(self.file_view_test.text(), self.file.get_name())

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_one_click(self, mock_dialog):
        """ Test if the function with just one click
        does not trigger the double click function"""
        self.file_view_test.click()
        mock_dialog.assert_not_called()

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_double_click(self, mock_dialog):
        """ Check that with a double click the function
        gets called"""
        self.file_view_test.click()
        self.file_view_test.click()
        mock_dialog.assert_called_once()

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_triple_click(self, mock_dialog):
        """ Check that with a triple click the function
        gets called"""
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 2)

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_quad_click(self, mock_dialog):
        """ Check that with a triple click the function
        gets called"""
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 3)
