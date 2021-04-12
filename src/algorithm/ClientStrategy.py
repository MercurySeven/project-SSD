from src.algorithm import tree_comparator
from src.algorithm.Strategy import Strategy
from src.algorithm.Strategy import common_code


class ClientStrategy(Strategy):
    def execute(self, logger, snapshot, client):
        # CLIENT = SNAPSHOT
        # SERVER = CLIENT
        result = tree_comparator.compareFolders(snapshot, client)
        if len(result) == 0:
            logger.info("Snapshot e client sono uguali")
        for r in result:
            common_code(r, logger)
