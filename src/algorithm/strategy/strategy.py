import os
from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional
from PySide2.QtCore import QSettings

from src.algorithm import os_handler, tree_builder
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.tree_node import TreeNode


def common_strategy(node_raw: dict, logger: Logger) -> None:
    # CLIENT = SNAPSHOT
    # SERVER = CLIENT
    action: Actions = node_raw["action"]
    node: TreeNode = node_raw["node"]
    name_node = node.get_name()

    if action == Actions.CLIENT_NEW_FOLDER:
        # Elimina nel server la cartella
        node_id = check_node_still_exists(node.get_path())
        if node_id is not None:
            if os_handler.delete_node(node_id, False):
                logger.info(f"Eliminata nel server la cartella: {name_node}")
    elif action == Actions.CLIENT_NEW_FILE:
        # Elimina nel server il file
        node_id = check_node_still_exists(node.get_path())
        if node_id is not None:
            if os_handler.delete_node(node_id, True):
                logger.info(f"Eliminato nel server il file: {name_node}")
    elif action == Actions.SERVER_NEW_FOLDER:
        # Il client ha una nuova cartella che deve essere caricata nel server
        parent_id = get_or_create_folder_id(node_raw["path"])
        os_handler.upload_folder(node, parent_id)
        logger.info(f"Nuova cartella da caricare nel server: {name_node}")
    elif action == Actions.SERVER_NEW_FILE:
        # Il client ha un nuovo file che deve essere caricato nel server
        parent_id = get_or_create_folder_id(node_raw["path"])
        os_handler.upload_file(node, parent_id)
        logger.info(f"Nuovo file da caricare nel server: {name_node}")


def check_node_still_exists(path: str) -> Optional[str]:
    """Ritorna un id se un nodo è presente, None altrimenti"""
    env_settings = QSettings()
    path_folder = env_settings.value("sync_path")
    result = os.path.relpath(path, path_folder)
    node_name = result.split(os.sep)

    current_node = tree_builder.get_tree_from_node_id()
    trovato = False
    for name in node_name:
        trovato = False
        for node in current_node.get_children():
            if node.get_name() == name:
                current_node = node
                trovato = True
                break
    if trovato:
        return current_node.get_payload().id
    return None


def get_or_create_folder_id(path: str) -> str:
    """Ritorna l'id della cartella dove vuoi inserire il file, se non presente ne crea una"""
    env_settings = QSettings()
    path_folder = env_settings.value("sync_path")
    if os.path.isfile(path):
        dir_path = os.path.dirname(path)
    else:
        dir_path = path
    result = os.path.relpath(dir_path, path_folder)
    node_name = result.split(os.sep)
    # Elimino il punto che mette se siamo nello stesso livello
    node_name = [name for name in node_name if name != "."]

    current_node = tree_builder.get_tree_from_node_id()
    index = 0
    for name in node_name:
        trovato = False
        for node in current_node.get_children():
            if node.get_name() == name:
                current_node = node
                trovato = True
                break
        if not trovato and index < len(node_name):
            id_new_folder = os_handler.create_folder(name, current_node.get_payload().id)
            current_node = tree_builder.get_tree_from_node_id(id_new_folder)
        index = index + 1

    return current_node.get_payload().id


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


class Strategy(ABC):
    @abstractmethod
    def execute(self, result_actions: list, logger: Logger) -> None:
        pass
