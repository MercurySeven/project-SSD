from logging import Logger
from .strategy import Strategy, common_strategy


class ClientStrategy(Strategy):
    def execute(self, result_actions: list, logger: Logger) -> None:
        for node_raw in result_actions:
            common_strategy(node_raw, logger)
