from unittest.mock import patch

from src.algorithm.strategy.client_strategy import ClientStrategy
from src.algorithm.strategy.manual_strategy import ManualStrategy
from src.algorithm.tree_comparator import Actions
from tests import default_code


class StrategyTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super(StrategyTest, self).setUp()
        self.client_strategy = ClientStrategy()
        self.manual_strategy = ManualStrategy()

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
