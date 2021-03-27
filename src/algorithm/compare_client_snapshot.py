import os
import logging
from PySide6.QtCore import QSettings

from . import tree_builder, tree_comparator, transfer_handler
from .tree_comparator import Actions
from src.model.network.tree_node import TreeNode


logger = logging.getLogger("decision_engine")


def compare_snap_client(snapshot: TreeNode, client: TreeNode) -> None:
    # CLIENT = SNAPSHOT
    # SERVER = CLIENT
    result = tree_comparator.compareFolders(snapshot, client)
    if len(result) == 0:
        logger.info("Snapshot e client sono uguali")
    for r in result:
        action: Actions = r["action"]
        node: TreeNode = r["node"]
        name_node = node.get_name()

        if action == Actions.CLIENT_NEW_FOLDER:
            # Elimina nel server la cartella
            node_id = get_id_from_path(node.get_payload().path)
            transfer_handler.delete_node(node_id)
            logger.info(f"Eliminata nel server la cartella: {name_node}")
        elif action == Actions.CLIENT_NEW_FILE:
            # Elimina nel server il client
            node_id = get_id_from_path(node.get_payload().path)
            transfer_handler.delete_node(node_id)
            logger.info(f"Eliminato nel server il file: {name_node}")
        elif action == Actions.SERVER_NEW_FOLDER:
            # Il client ha una nuova cartella che deve essere caricata nel server
            parent_id = get_id_from_path(r["path"])
            transfer_handler.upload_folder(node, parent_id)
            logger.info(f"Nuova cartella da caricare nel server: {name_node}")
        elif action == Actions.SERVER_NEW_FILE:
            # Il client ha un nuovo file che deve essere caricato nel server
            parent_id = get_id_from_path(r["path"])
            transfer_handler.upload_file(node, parent_id)
            logger.info(f"Nuovo file da caricare nel server: {name_node}")
        # elif action == Actions.SERVER_UPDATE_FILE:
            # Il client ha un file aggiornato rispetto allo snapshot
            # TODO: Per la policy manuale, prendo la data dello snapshot del file, la confronto
            # con la data del server, se quella del server è diversa significa che ho avuto un
            # upload nel mentre ero offline.
            # parent_id = get_id_from_path(r["path"])
            # transfer_handler.upload_file(node, parent_id)
            # logger.info(f"File aggiornato rispetto lo snapshot, carico nel server: {name_node}")


def get_id_from_path(path: str) -> str:
    env_settings = QSettings()
    path_folder = env_settings.value("sync_path")
    result = os.path.relpath(path, path_folder)
    node_name = result.split(os.sep)

    current_node = tree_builder.get_tree_from_node_id()
    for name in node_name:
        for node in current_node.get_children():
            if node.get_name() == name:
                current_node = node
                break
    return current_node.get_payload().id
