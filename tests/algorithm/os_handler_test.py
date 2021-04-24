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
        os_handler.set_model(self.main_model.network_model)

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
        os_handler.set_model(None)
        self.assertIsNone(os_handler.networkmodel)
        os_handler.set_model(self.main_model.network_model)
        self.assertEqual(os_handler.networkmodel, self.main_model.network_model)

    @patch('src.model.network_model.NetworkModel.download_node', return_value=None)
    def test_download_folder_with_file(self, mocked_fun):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.Folder, created, updated, self.path))
        test_node.add_node(TreeNode(Node("CLIENT_NODE", self.file_name,
                                         Type.File, created, updated, self.path)))
        os_handler.download_folder(test_node, self.path)
        mocked_fun.assert_called_once()
        self.assertTrue(os.path.exists(os.path.join(self.path, self.folder_name)))

    def test_download_folder_with_folder(self):
        created = 100
        updated = 200
        test_node = TreeNode(Node("CLIENT_NODE", self.folder_name,
                                  Type.Folder, created, updated, self.path))
        test_node.add_node(TreeNode(Node("CLIENT_NODE", self.folder_name,
                                         Type.Folder, created, updated, self.path)))
        os_handler.download_folder(test_node, self.path)
        folder_path = os.path.join(self.path, self.folder_name)
        inner_folder_path = os.path.join(folder_path, self.folder_name)
        self.assertTrue(os.path.exists(folder_path))
        self.assertTrue(os.path.exists(inner_folder_path))

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

    @patch('src.model.network_model.NetworkModel.delete_node')
    def test_delete_node(self, mocked_fun):
        os_handler.delete_node("test")
        mocked_fun.assert_called_once()
