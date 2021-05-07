from tests import default_code
from unittest.mock import patch
from src.view.remote_file_view import RemoteFileView
from src.model.main_model import MainModel


class RemoteFileViewTest(default_code.DefaultCode):

    @patch(
        'src.algorithm.tree_builder.get_tree_from_node_id',
        return_value=default_code.create_folder_with_files(
            ["default_test1", "default_test2", "default_test3"]))
    def setUp(self, mock) -> None:
        super().setUp()

        self.main_model = MainModel()
        self.main_model.remote_file_model
        self.file_view_test = RemoteFileView(self.main_model)

    def tearDown(self) -> None:
        super().tearDown()

    @patch(
        'src.algorithm.tree_builder.get_tree_from_node_id',
        return_value=default_code.create_folder_with_files(
            ["test1", "test2", "test3"]))
    def test_model_changed_files(self, mock):
        self.file_view_test.Sl_model_changed()
        test_list = self.file_view_test.fileLayout._item_list
        self.assertEqual(test_list[0].wid.name == "test1", True)
        self.assertEqual(test_list[1].wid.name == "test2", True)
        self.assertEqual(test_list[2].wid.name == "test3", True)

    @patch(
        'src.algorithm.tree_builder.get_tree_from_node_id',
        return_value=default_code.create_folder_with_folders(
            ["test1", "test2", "test3"]))
    def test_model_changed_dirs(self, mock):
        self.file_view_test.Sl_model_changed()
        test_list = self.file_view_test.fileLayout._item_list
        self.assertEqual(test_list[0].wid.name == "test1", True)
        self.assertEqual(test_list[1].wid.name == "test2", True)
        self.assertEqual(test_list[2].wid.name == "test3", True)

    @patch(
        'src.algorithm.tree_builder.get_tree_from_node_id',
        return_value=default_code.create_folder_with_files(
            ["test1", "test2", "test3"]))
    def test_refresh_button(self, mock):
        result = self.file_view_test._model.folder_queue = ["NOT_LOCAL_ROOT"]
        self.file_view_test.Sl_refresh_button_clicked()
        result = self.file_view_test._model.folder_queue == ["LOCAL_ROOT"]
        self.assertEqual(result, True)

    def test_add_sync_file_exists(self):
        self.file_view_test.Sl_add_sync_file("test")

    def test_remove_sync_file_exists(self):
        self.file_view_test.Sl_remove_sync_file("test")

    def test_file_status_changed_exists(self):
        self.file_view_test.Sl_file_status_changed()
