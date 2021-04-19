import os
from logging import Logger
from PySide6.QtCore import QSettings
from .strategy import Strategy, common_strategy
from src.algorithm import os_handler, tree_builder
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.tree_node import TreeNode


class ClientStrategy(Strategy):
    def execute(self, result_actions: list, logger: Logger) -> None:
        # CLIENT = SNAPSHOT
        # SERVER = CLIENT
        for node_raw in result_actions:
            action: Actions = node_raw["action"]
            node: TreeNode = node_raw["node"]
            name_node = node.get_name()

            if action == Actions.SERVER_UPDATE_FILE:
                # Il client ha un file aggiornato rispetto allo snapshot
                node_id = self.try_get_id_from_path(node.get_payload().path)
                os_handler.upload_file(node, node_id)
                logger.info(action.name + " " + name_node)
            else:
                common_strategy(node_raw, logger)

    def try_get_id_from_path(self, path: str) -> str:
        env_settings = QSettings()
        path_folder = env_settings.value("sync_path")
        result = os.path.relpath(path, path_folder)
        node_name = result.split(os.sep)

        current_node = tree_builder.get_tree_from_node_id()
        index = 0
        for name in node_name:
            trovato = False
            for node in current_node.get_children():
                if node.get_name() == name:
                    current_node = node
                    trovato = True
                    break
            if not trovato and index < len(node_name) - 1:
                id_new_folder = os_handler.create_folder(name, current_node.get_payload().id)
                current_node = tree_builder.get_tree_from_node_id(id_new_folder)
            index = index + 1
        return current_node.get_payload().id
