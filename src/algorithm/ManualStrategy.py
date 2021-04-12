from src.algorithm import tree_comparator
from src.algorithm.Strategy import Strategy, common_code
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.tree_node import TreeNode


class ManualStrategy(Strategy):
    def execute(self, logger, snapshot, client):
        # CLIENT = SNAPSHOT
        # SERVER = CLIENT
        result = tree_comparator.compareFolders(snapshot, client)
        if len(result) == 0:
            logger.info("Snapshot e client sono uguali")
        for r in result:
            action: Actions = r["action"]
            node: TreeNode = r["node"]
            # name_node =
            node.get_name()

            if action == Actions.SERVER_UPDATE_FILE:
                # Il client ha un file aggiornato rispetto allo snapshot
                # TODO: Per la policy manuale, prendo la data dello snapshot del file, la confronto
                # con la data del server, se quella del server è diversa significa che ho avuto un
                # upload nel mentre ero offline.
                # node_id = get_id_from_path(node.get_payload().path)
                # node_metadata = os_handler.networkmodel.get_content_from_node(node_id)
                # print(node_metadata)
                pass
            else:
                common_code(r, logger)
