from logging import Logger

from PySide6.QtCore import (QObject, Signal)

from .strategy import Strategy, common_strategy, get_id_from_path
from src.algorithm import os_handler, tree_builder
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.tree_node import TreeNode
from src.model.algorithm.node import Node


class ManualStrategyMeta(type(QObject), type(Strategy)):
    pass


class ManualStrategy(Strategy, QObject, metaclass=ManualStrategyMeta):
    Sg_set_nodes = Signal(Node, Node)

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
                node_json = os_handler.network_model.get_content_from_node(node_id)
                node_server = tree_builder._create_node_from_dict(node_json["getNode"])
                node_last_update_server = node_server.get_updated_at()
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
                    self.Sg_set_nodes.emit(node.get_payload(), node_server.get_payload())
                    # res = conflict_messagebox.exec_()
                    # if res == 0:
                    #     # Mantieni modifiche client
                    #     print("CLIENT")
                    # else:
                    #     # Mantieni modifiche server
                    #     print("SERVER")
            else:
                common_strategy(node_raw, logger)
