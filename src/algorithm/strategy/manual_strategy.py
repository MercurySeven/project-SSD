import math
from logging import Logger
from .strategy import Strategy, common_strategy, get_id_from_path
from src.algorithm import os_handler
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.tree_node import TreeNode


class ManualStrategy(Strategy):
    def execute(self, result_actions: list, logger: Logger) -> None:
        # CLIENT = SNAPSHOT
        # SERVER = CLIENT
        for node_raw in result_actions:
            action: Actions = node_raw["action"]
            node: TreeNode = node_raw["node"]
            name_node = node.get_name()

            if action == Actions.SERVER_UPDATE_FILE:
                # Il client ha un file aggiornato rispetto allo snapshot
                # Per la policy manuale, prendo la data dello snapshot del file, la confronto
                # con la data del server, se quella del server è diversa significa che ho avuto un
                # upload nel mentre ero offline.
                node_id = get_id_from_path(node.get_payload().path)
                node_metadata = os_handler.networkmodel.get_content_from_node(node_id)
                last_update_raw = node_metadata["getNode"]["updated_at"]
                node_last_update_server = math.trunc(last_update_raw / 1000)
                snap_last_update = node_raw["snap_last_update"]
                if snap_last_update == node_last_update_server:
                    """L'utente ha modificato il file aggiornato rispetto al server, non ci
                    saranno perdite di informazioni"""
                    node_id = super().get_or_create_folder_id(node.get_payload().path)
                    os_handler.upload_file(node, node_id)
                    logger.info("File aggiornato, effettuato l'upload " + name_node)
                else:
                    """Nel mentre l'utente modificava il file,nel server è avvenuto un caricamento.
                    Chiedere all'utente come vuole procedere"""
                    pass
            else:
                common_strategy(node_raw, logger)
