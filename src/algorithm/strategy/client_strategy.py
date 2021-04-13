from logging import Logger
from .strategy import Strategy, common_code


class ClientStrategy(Strategy):
    def execute(self, result_actions: list, logger: Logger) -> None:
        for action in result_actions:
            common_code(action, logger)
