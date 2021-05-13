import os
import pathlib
from unittest.mock import patch

from src.algorithm import os_handler
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from src.model.main_model import MainModel
from tests import default_code


class OsHandlerTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()
        self.env_settings = super().get_env_settings()
        self.main_model = MainModel()
        os_handler.set_network_model(self.main_model.network_model)
        os_handler.set_settings_model(self.main_model.settings_model)

        self.original_path = self.env_settings.value(super().SYNC_ENV_VARIABLE)
        self.folder_name = "test"
        self.file_name = "test.txt"

        self.path = os.path.join(self.original_path, "tree")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

    def delete_files(self):
        folder_to_remove = os.path.join(self.path, self.folder_name)
        file_to_remove = os.path.join(folder_to_remove, self.file_name)
        optional_folder = os.path.join(folder_to_remove, self.folder_name)

        try:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
        except Exception as e:
            print(e)
        try:
            if os.path.exists(optional_folder):
                os.rmdir(optional_folder)
        except Exception as e:
            print(e)
        try:
            if os.path.exists(folder_to_remove):
                os.rmdir(folder_to_remove)
        except Exception as e:
            print(e)
        try:
            if os.path.exists(self.path):
                os.rmdir(self.path)
        except Exception as e:
            print(e)

    def tearDown(self) -> None:
        self.delete_files()
        super().tearDown()

    def test_set_model(self):
        os_handler.set_network_model(None)
        self.assertIsNone(os_handler.network_model)
        os_handler.set_network_model(self.main_model.network_model)
        self.assertEqual(os_handler.network_model, self.main_model.network_model)

    @patch('src.model.network_model.NetworkModel.download_node', return_value=True)
    @patch('src.model.settings_model.SettingsModel.is_id_in_sync_list', return_value=True)
    @patch('src.algorithm.os_handler.check_node_in_nodelist', return_value=True)
    def test_download_folder_with_file(self, mock_1, mock_2, mock_3):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.Folder, created, updated, self.path))
        test_node.add_node(TreeNode(Node("CLIENT_NODE", self.file_name,
                                         Type.File, created, updated, self.path)))
        x = os_handler.download_folder(test_node, self.path)
        self.assertEqual(x, [True])
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    def test_download_folder_with_folder(self):
        created = 100
        updated = 200
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.Folder, created, updated, self.path))
        test_node.add_node(TreeNode(Node("CLIENT_NODE", self.folder_name,
                                         Type.Folder, created, updated, self.path)))
        x = os_handler.download_folder(test_node, self.path)
        self.assertEqual(x, [])
        folder_path = os.path.join(self.path, self.folder_name)
        inner_folder_path = os.path.join(folder_path, self.folder_name)
        self.assertEqual(os.path.exists(folder_path), False)
        self.assertEqual(os.path.exists(inner_folder_path), False)

    @patch('src.model.network_model.NetworkModel.upload_node', return_value=None)
    @patch('src.model.network_model.NetworkModel.create_folder', return_value=None)
    def test_upload_folder_with_file(self, mocked_create, mocked_upload):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.Folder, created, updated, self.path))
        test_node.add_node(TreeNode(Node("CLIENT_NODE", self.file_name,
                                         Type.File, created, updated, self.path)))
        os_handler.upload_folder(test_node, self.path)
        mocked_upload.assert_called_once()
        mocked_create.assert_called_once()

    @patch('src.model.network_model.NetworkModel.create_folder', return_value=None)
    def test_upload_folder_with_folder(self, mocked_fun):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.Folder, created, updated, self.path))
        test_node.add_node(TreeNode(Node("CLIENT_NODE", self.file_name,
                                         Type.Folder, created, updated, self.path)))
        os_handler.upload_folder(test_node, self.path)
        self.assertEqual(mocked_fun.call_count, 2)

    @patch('src.model.settings_model.SettingsModel.is_id_in_sync_list', return_value=False)
    def test_download_file_not_in_list(self, mocked_fun):
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.File, 100, 200, "ciao.txt"))
        res = os_handler.download_file(test_node, self.path)
        mocked_fun.assert_called_once()
        self.assertIsNone(res)

    @patch('src.model.settings_model.SettingsModel.get_sync_list', return_value=["a", "b"])
    @patch('src.model.network_model.NetworkModel.delete_node')
    def test_delete_node_file_present(self, m1, m2):
        res = os_handler.delete_node("a", True)
        m1.assert_called_once()
        m2.assert_called_once()
        self.assertTrue(res)

    @patch('src.model.settings_model.SettingsModel.get_sync_list', return_value=["a", "b"])
    def test_delete_node_file_not_present(self, m1):
        res = os_handler.delete_node("c", True)
        m1.assert_called_once()
        self.assertFalse(res)
