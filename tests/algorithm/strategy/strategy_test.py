import os
import pathlib
from unittest.mock import patch

from src.algorithm import os_handler
from src.algorithm.strategy.client_strategy import ClientStrategy
from src.algorithm.strategy.manual_strategy import ManualStrategy
from src.algorithm.tree_comparator import Actions
from src.model.main_model import MainModel
from tests import default_code


class StrategyTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super(StrategyTest, self).setUp()
        self.client_strategy = ClientStrategy()
        self.manual_strategy = ManualStrategy()
        # setup per manual strategy
        os_handler.set_network_model(MainModel().network_model)
        self.env_set = super().get_env_settings()

        # create files
        self.original_path = self.env_settings.value(super().SYNC_ENV_VARIABLE)
        self.folder_name = "test"
        self.file_name = "test.txt"

        self.path = os.path.join(self.original_path, "tree")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        self.first_folder = os.path.join(self.path, self.folder_name)
        pathlib.Path(self.first_folder).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(self.first_folder, self.file_name), "w"):
            pass

    def delete_files(self):
        file_to_remove = os.path.join(self.first_folder, self.file_name)

        try:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
        except Exception as e:
            print(e)
        try:
            if os.path.exists(self.first_folder):
                os.rmdir(self.first_folder)
        except Exception as e:
            print(e)
        try:
            if os.path.exists(self.path):
                os.rmdir(self.path)
        except Exception as e:
            print(e)

    def tearDown(self) -> None:
        self.delete_files()
        super(StrategyTest, self).tearDown()

    @patch('src.algorithm.strategy.strategy.Strategy.get_or_create_folder_id', return_value=None)
    @patch('src.algorithm.os_handler.upload_file')
    def test_execute_client_strategy_server_update_file(self, mock_1, mock_2):
        obj_to_iterate: list = [default_code.ResultObj(Actions.SERVER_UPDATE_FILE).result]
        logger = default_code.FakeLogger()
        self.client_strategy.execute(obj_to_iterate, logger)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.algorithm.strategy.client_strategy.common_strategy')
    def test_execute_client_strategy_common(self, mock_1):
        obj_to_iterate: list = [default_code.ResultObj(Actions.CLIENT_UPDATE_FILE).result,
                                default_code.ResultObj(Actions.CLIENT_NEW_FOLDER).result,
                                default_code.ResultObj(Actions.CLIENT_NEW_FILE).result,
                                default_code.ResultObj(Actions.SERVER_NEW_FOLDER).result,
                                default_code.ResultObj(Actions.SERVER_NEW_FILE).result]
        logger = default_code.FakeLogger()
        self.client_strategy.execute(obj_to_iterate, logger)
        self.assertEqual(mock_1.call_count, 5)

    @patch('src.model.network_model.NetworkModel.get_content_from_node',
           return_value=default_code.NodeMetadata().get_content_from_node())
    @patch('src.algorithm.strategy.strategy.Strategy.get_or_create_folder_id', return_value=None)
    @patch('src.algorithm.os_handler.upload_file')
    @patch('src.algorithm.strategy.manual_strategy.get_id_from_path', return_value="id")
    def test_execute_manual_strategy_server_update_file_equals_snap(
            self, mock_1, mock_2, mock_3, mock_4):
        obj_to_iterate: list = [default_code.ResultObj(Actions.SERVER_UPDATE_FILE).result]
        logger = default_code.FakeLogger()
        self.manual_strategy.execute(obj_to_iterate, logger)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()
        mock_4.assert_called_once()

    @patch('src.model.network_model.NetworkModel.get_content_from_node',
           return_value=default_code.NodeMetadata(2000).get_content_from_node())
    @patch('src.algorithm.strategy.manual_strategy.get_id_from_path', return_value="id")
    def test_execute_manual_strategy_server_update_file_diff_snap(
            self, mock_1, mock_2):
        obj_to_iterate: list = [default_code.ResultObj(Actions.SERVER_UPDATE_FILE).result]
        logger = default_code.FakeLogger()
        self.manual_strategy.execute(obj_to_iterate, logger)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.algorithm.strategy.manual_strategy.common_strategy')
    def test_execute_manual_strategy_common(self, mock_1):
        logger = default_code.FakeLogger()
        obj_to_iterate: list = [default_code.ResultObj(Actions.CLIENT_UPDATE_FILE).result,
                                default_code.ResultObj(Actions.CLIENT_NEW_FOLDER).result,
                                default_code.ResultObj(Actions.CLIENT_NEW_FILE).result,
                                default_code.ResultObj(Actions.SERVER_NEW_FOLDER).result,
                                default_code.ResultObj(Actions.SERVER_NEW_FILE).result]
        self.manual_strategy.execute(obj_to_iterate, logger)
        self.assertEqual(mock_1.call_count, 5)

    @patch('src.algorithm.os_handler.create_folder')
    @patch('src.algorithm.tree_builder.get_tree_from_node_id',
           return_value=default_code._get_file_test_node())
    def test_get_or_create_id_empty(self, get_tree_mock, create_folder_mock):
        client_result = self.client_strategy.get_or_create_folder_id(
            self.env_set.value(default_code.DefaultCode.SYNC_ENV_VARIABLE))
        create_folder_mock.assert_called_once()
        self.assertEqual(get_tree_mock.call_count, 2)
        manual_result = self.manual_strategy.get_or_create_folder_id(
            self.env_set.value(default_code.DefaultCode.SYNC_ENV_VARIABLE))
        self.assertEqual(create_folder_mock.call_count, 2)
        self.assertEqual(get_tree_mock.call_count, 4)
        self.assertEqual(client_result, manual_result)

    @patch('src.algorithm.tree_builder.get_tree_from_node_id',
           return_value=default_code.create_folder_with_folders(["tree", "tree"]))
    def test_get_or_create_id_found(self, get_tree_mock):
        client_result = self.client_strategy.get_or_create_folder_id(self.first_folder)
        self.assertEqual(get_tree_mock.call_count, 1)
        manual_result = self.manual_strategy.get_or_create_folder_id(self.first_folder)
        self.assertEqual(get_tree_mock.call_count, 2)
        self.assertEqual(client_result, manual_result)

    @patch('src.algorithm.os_handler.create_folder')
    @patch('src.algorithm.tree_builder.get_tree_from_node_id',
           return_value=default_code.create_folder_with_folders(["x", "x"]))
    def test_get_or_create_id_not_found(self, get_tree_mock, create_folder_mock):
        client_result = self.client_strategy.get_or_create_folder_id(self.first_folder)
        create_folder_mock.assert_called_once()
        self.assertEqual(get_tree_mock.call_count, 2)
        manual_result = self.manual_strategy.get_or_create_folder_id(self.first_folder)
        self.assertEqual(create_folder_mock.call_count, 2)
        self.assertEqual(get_tree_mock.call_count, 4)
        self.assertEqual(client_result, manual_result)
