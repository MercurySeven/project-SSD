import os

from logging import Logger
from .strategy import Strategy, common_strategy, get_id_from_path, get_or_create_folder_id
from src.algorithm import os_handler, tree_builder
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
                node_json = os_handler.network_model.get_content_from_node(node_id)
                node_server = tree_builder._create_node_from_dict(node_json["getNode"])
                node_last_update_server = node_server.get_updated_at()
                snap_last_update = node_raw["snap_last_update"]

                # Devo fare il controllo per Trinity, verificare che
                # il nodo non sia stato cancellato
                is_different_node = node_server.get_name() != name_node
                if snap_last_update == node_last_update_server or is_different_node:
                    """L'utente ha modificato il file aggiornato rispetto al server, non ci
                    saranno perdite di informazioni"""
                    node_id = get_or_create_folder_id(node.get_payload().path)
                    os_handler.upload_file(node, node_id)
                    logger.info("File aggiornato, effettuato l'upload " + name_node)
                else:
                    """Nel mentre l'utente modificava il file, nel server è avvenuto un caricamento.
                    1. Il file che l'utente ha, viene rinominato in FileA(client).txt
                    2. Il FileA(client).txt va caricato nel server
                    3. Viene scaricato il file FileA.txt
                    4. Viene mandata una notifica?"""

                    # Rinominare il file aggiungendo (client)
                    old_path = node.get_payload().path
                    dir_path = os.path.dirname(old_path)
                    vett_supp = name_node.split(".")
                    new_file_name = vett_supp[0] + " (client)." + vett_supp[1]
                    new_path = os.path.join(dir_path, new_file_name)
                    os.rename(old_path, new_path)

                    # Ricostruisco il nodo e name_node
                    node = tree_builder._build_tree_node(new_path, new_file_name)
                    name_node = node.get_name()

                    # Effettuo l'upload
                    node_id = get_or_create_folder_id(node.get_payload().path)
                    os_handler.upload_file(node, node_id)

                    # Il file che è stato modificato dall'altro client, viene scaricato dopo
                    # in decision_engine.py

            else:
                common_strategy(node_raw, logger)
