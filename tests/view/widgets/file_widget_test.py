import os
import time

from src.algorithm.tree_builder import _build_tree_node
from src.model.widgets.local_file import LocalFile
from src.model.widgets.file import File
from unittest.mock import patch

from src.view.widgets.local_file_widget import LocalFileWidget
from src.view.widgets.file_widget import FileWidget
from tests import default_code


class FileWidgetTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()
        self.env_settings = super().get_env_settings()
        self.path = self.env_settings.value(self.SYNC_ENV_VARIABLE)
        self.file_name = os.path.join(self.path, "prova.txt")
        with open(self.file_name, "w"):
            pass
        self.tree = _build_tree_node(self.file_name, "prova.txt")
        self.file = LocalFile(self.tree)
        self.file_view_test = LocalFileWidget(self.file)

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

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_one_click(self, mock_dialog):
        """ Test if the function with just one click
        does not trigger the double click function"""
        self.file_view_test.click()
        mock_dialog.assert_not_called()

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_double_click(self, mock_dialog):
        """ Check that with a double click the function
        gets called"""
        self.file_view_test.click()
        self.file_view_test.click()
        mock_dialog.assert_called_once()

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_triple_click(self, mock_dialog):
        """ Check that with a triple click the function
        gets called"""
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 2)

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_quad_click(self, mock_dialog):
        """ Check that with a triple click the function
        gets called"""
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 3)

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_click_pause500_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        mock_dialog.assert_not_called()

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_click_pause050_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.050)
        self.file_view_test.click()
        mock_dialog.assert_called_once()

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_click_pause_double_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        self.file_view_test.click()
        mock_dialog.assert_called_once()

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_click_pause_triple_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 2)

    @patch("PySide2.QtGui.QDesktopServices.openUrl")
    def test_click_pause_quad_click(self, mock_dialog):
        self.file_view_test.click()
        time.sleep(0.500)
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.file_view_test.click()
        self.assertEqual(mock_dialog.call_count, 3)

    def test_set_icon_video(self):
        self.file_view_test.extension = "mp4"
        self.file_view_test.set_icon()

    def test_set_icon_image(self):
        self.file_view_test.extension = "jpg"
        self.file_view_test.set_icon()

    def test_set_icon_audio(self):
        self.file_view_test.extension = "mp3"
        self.file_view_test.set_icon()

    def test_on_double_click_exists(self):
        test_file = File(default_code._get_test_node())
        test_widget = FileWidget(test_file)
        test_widget.Sl_on_double_click()
