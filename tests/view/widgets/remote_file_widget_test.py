from src.model.widgets.remote_file import RemoteFile
from src.model.main_model import MainModel
from src.view.remote_file_view import RemoteFileView
from unittest.mock import patch

from src.view.widgets.remote_file_widget import RemoteFileWidget
from tests import default_code


class RemoteFileWidgetTest(default_code.DefaultCode):

    @patch(
        'src.algorithm.tree_builder.get_tree_from_node_id',
        return_value=default_code._get_test_node())
    def setUp(self, mocked) -> None:
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()
        self.test_model = MainModel()
        self.test_file_view = RemoteFileView(self.test_model)
        self.test_file = RemoteFile(default_code._get_file_test_node("test"))
        self.test_file_widget = RemoteFileWidget(self.test_file, self.test_model.settings_model)

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""

    def test_double_click_present(self):
        self.test_model.settings_model.add_id_to_sync_list("CLIENT_NODE")
        self.test_file_widget.Sl_on_double_click()
        result = self.test_model.settings_model.is_id_in_sync_list(self.test_file.id)
        self.assertEqual(result, True)
        self.test_model.settings_model.remove_id_from_sync_list("CLIENT_NODE")

    def test_double_click_absent(self):
        self.test_model.settings_model.add_id_to_sync_list("NOT_CLIENT_NODE")
        self.test_file_widget.Sl_on_double_click()
        result = self.test_model.settings_model.is_id_in_sync_list(self.test_file.id)
        self.assertEqual(result, False)
        self.test_model.settings_model.remove_id_from_sync_list("NOT_CLIENT_NODE")

    @patch('PySide6.QtGui.QPainter.drawPixmap')
    def test_show_synced(self, mocked):
        self.test_file_widget.show_synced()
        mocked.assert_called()

    @patch('PySide6.QtGui.QPainter.drawPixmap')
    def test_files_status_changed_synced(self, mocked):
        self.test_model.settings_model.add_id_to_sync_list("CLIENT_NODE")
        self.test_file_widget.Sl_on_file_status_changed()
        mocked.assert_called()
        self.test_model.settings_model.remove_id_from_sync_list("CLIENT_NODE")

    @patch('PySide6.QtGui.QPainter.drawPixmap')
    def test_files_status_changed_not_synced(self, mocked):
        self.test_file_widget.Sl_on_file_status_changed()
        mocked.assert_not_called()
