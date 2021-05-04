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

    def tearDown(self) -> None:
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
