from logging import Logger
from .strategy import Strategy, common_strategy
from src.algorithm import os_handler
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.tree_node import TreeNode


class ClientStrategy(Strategy):
    def execute(self, result_actions: list, logger: Logger) -> None:
        # CLIENT = SNAPSHOT
        # SERVER = CLIENT
        for node_raw in result_actions:
            action: Actions = node_raw["action"]
            node: TreeNode = node_raw["node"]
            name_node = node.get_name()

            if action == Actions.SERVER_UPDATE_FILE:
                # Il client ha un file aggiornato rispetto allo snapshot
                path = node_raw["id"]
                os_handler.upload_file(node, path)
                logger.info(action.name + " " + name_node)
            else:
                common_strategy(node_raw, logger)
