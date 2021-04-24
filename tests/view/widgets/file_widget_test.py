import os
import time

from src.algorithm.tree_builder import _build_tree_node
from src.model.widgets.file import File
from src.view.widgets.file_widget import FileWidget
from unittest.mock import patch

from tests import default_code


class FileWidgetTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()
        self.env_settings = super().get_env_settings()
        self.path = self.env_settings.value(self.SYNC_ENV_VARIABLE)
        self.file_name = os.path.join(self.path, "prova.txt")
        with open(self.file_name, "w"):
            pass
        self.tree = _build_tree_node(self.file_name, "prova")
        self.file = File(self.tree)
        self.file_view_test = FileWidget(self.file)

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(os.path.join(self.path, "prova.txt"))
        super().tearDown()

    def test_defaults(self):
        """ Test file_widget default values"""
        # to_compare = "Ultima modifica: " + self.file.get_last_modified_date() + "\nSize: " + \
        #    self.file.get_size()
        self.assertEqual(self.file_view_test.accessibleName(), "File")
        # self.assertEqual(self.file_view_test.toolTip(), to_compare)
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

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_click_pause500_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        mock_dialog.assert_not_called()

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_click_pause050_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.050)
        self.file_view_test.click()
        mock_dialog.assert_called_once()

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_click_pause_double_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        self.file_view_test.click()
        mock_dialog.assert_called_once()

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_click_pause_triple_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 2)

    @patch("PySide6.QtGui.QDesktopServices.openUrl")
    def test_click_pause_quad_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 3)
