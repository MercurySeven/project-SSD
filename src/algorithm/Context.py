import logging

from src import settings
from src.algorithm.ClientStrategy import ClientStrategy
from src.algorithm.ManualStrategy import ManualStrategy
from src.algorithm.Strategy import Strategy
from src.model.algorithm.policy import Policy
from src.model.algorithm.tree_node import TreeNode


class Context:
    strategy: Strategy
    logger = logging.getLogger("decision_engine")

    def update_strategy(self):
        policy = Policy(settings.get_policy())
        if policy == Policy.Client:
            self.strategy: Strategy = ClientStrategy()
        else:
            self.strategy: Strategy = ManualStrategy()

    def compare_snap_client(self, snapshot: TreeNode, client: TreeNode) -> None:
        self.update_strategy()
        return self.strategy.execute(self.logger, snapshot, client)
