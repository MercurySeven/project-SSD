import logging

from src.algorithm.strategy.strategy import Strategy
from src.model.algorithm.tree_node import TreeNode
from src.algorithm import tree_comparator


class CompareSnapClient:
    logger = logging.getLogger("decision_engine")

    def check(self, snapshot: TreeNode, client: TreeNode, strategy: Strategy) -> bool:
        """Ritorna un bool per indicare se sono state fatte operazioni tra i 2 alberi"""
        result_actions = tree_comparator.compareFolders(snapshot, client)
        if len(result_actions) == 0:
            self.logger.info("Snapshot e client sono uguali")
            return False
        else:
            strategy.execute(result_actions, self.logger)
            return True
