from . import tree_builder, tree_comparator, transfer_handler
from .tree_comparator import Actions
from src.model.network.tree_node import TreeNode
from src.network import api
from PySide6.QtCore import QSettings
import os


def compare_snap_client(snapshot: TreeNode, client: TreeNode) -> None:
    # CLIENT = SNAPSHOT
    # SERVER = CLIENT
    result = tree_comparator.compareFolders(snapshot, client)
    if len(result) == 0:
        print("Snapshot e client sono uguali")
    for r in result:
        action: Actions = r["action"]
        node: TreeNode = r["node"]

        if action == Actions.CLIENT_NEW_FOLDER:
            # Elimina nel server la cartella
            node_id = get_id_from_path(node._payload.path)
            api.delete_node(node_id)
            print("Eliminata nel server la cartella: " + node.get_name())
        elif action == Actions.CLIENT_NEW_FILE:
            # Elimina nel server il client
            node_id = get_id_from_path(node._payload.path)
            api.delete_node(node_id)
            print("Eliminato nel server il file: " + node.get_name())
        # elif action == Actions.CLIENT_UPDATE_FILE:
        #     # In teoria non può succedere, lo snapshot non può avere una data di ultima
        #     # modifica più recente
        #     # path = r["id"]
        #     # transfer_handler.upload_file(node, path)
        elif action == Actions.SERVER_NEW_FOLDER:
            # Il client ha una nuova cartella che deve essere caricata nel server
            parent_id = get_id_from_path(r["path"])
            transfer_handler.upload_folder(node, parent_id)
        elif action == Actions.SERVER_NEW_FILE:
            # Il client ha un nuovo file che deve essere caricato nel server
            parent_id = get_id_from_path(r["path"])
            transfer_handler.upload_file(node, parent_id)
        # elif action == Actions.SERVER_UPDATE_FILE:
            # Il client ha un file aggiornato rispetto allo snapshot
            # path = r["path"]
            # transfer_handler.download_file(node, path)


def get_id_from_path(path: str) -> str:
    env_settings = QSettings()
    path_folder = env_settings.value("sync_path")
    result = os.path.relpath(path, path_folder)
    node_name = result.split(os.sep)

    current_node = tree_builder.get_tree_from_node_id()
    for name in node_name:
        for node in current_node._children:
            if node.get_name() == name:
                current_node = node
                break
    return current_node._payload.id
