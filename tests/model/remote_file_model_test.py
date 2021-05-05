from unittest.mock import patch

from src.model.main_model import MainModel
from src.algorithm import tree_builder
from tests import default_code
from src.network.api_exceptions import APIException

class RemoteFileModelTest(default_code.DefaultCode):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()
        self.main_model = MainModel()
        self.model_test = self.main_model.remote_file_model

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()
        self.model_test.folder_queue.clear()
        self.model_test.folder_queue.append("LOCAL_ROOT")

    def test_set_network_model(self):
        network_model = self.main_model.network_model
        self.model_test.set_network_model(network_model)
        self.assertEqual(tree_builder.networkmodel, network_model)

    @patch('src.algorithm.tree_builder.get_tree_from_node_id', return_value=True)
    def test_get_current_tree(self, mocked_get_tree_from_node):
        result = self.model_test.get_current_tree()
        mocked_get_tree_from_node.assert_called_once()
        self.assertEqual(result, True)

    @patch(
        'src.model.remote_file_model.RemoteFileModel.get_current_tree',
        return_value=default_code.create_folder_with_files(
            ["TestFile"]))
    def test_get_data_file(self, mocked_get_tree_from_node):
        file_result, dir_result = self.model_test.get_data()
        self.assertEqual(file_result[-1].get_name(), "TestFile")

    @patch(
        'src.model.remote_file_model.RemoteFileModel.get_current_tree',
        return_value=default_code.create_folder_with_folders(
            ["TestFolder"]))
    def test_get_data_folder(self, mocked_get_tree_from_node):
        file_result, dir_result = self.model_test.get_data()
        self.assertEqual(dir_result[-1].get_name(), "TestFolder")

    @patch(
        'src.model.remote_file_model.RemoteFileModel.get_current_tree',
        return_value=default_code.create_folder_with_files(
            ["TestFile"]))
    def test_get_data_not_prev_dir(self, mocked_get_tree_from_node):
        self.model_test.folder_queue.append("NonRoot")
        file_result, dir_result = self.model_test.get_data()
        self.assertEqual(dir_result[0].get_name(), "..")

    @patch(
        'src.model.remote_file_model.RemoteFileModel.get_current_tree',
        return_value=default_code.create_folder_with_files(
            ["TestFile"]))
    def test_get_data_exception(self, mocked_get_tree_from_node):
        mocked_get_tree_from_node.side_effect = APIException
        test_result = self.model_test.get_data()
        self.assertEqual(test_result, None)

    def test_set_current_node_descend(self):
        self.model_test.set_current_node("TestNode")
        self.assertEqual(self.model_test.folder_queue[-1], "TestNode")

    def test_set_current_node_ascend(self):
        self.model_test.folder_queue.append("TestNode")
        self.model_test.folder_queue.append("SecondNode")
        self.model_test.set_current_node("SecondNode")
        self.assertEqual(self.model_test.folder_queue[-1], "TestNode")
