from threading import Thread
from time import sleep
import logging

from PySide6.QtCore import QSettings

from . import tree_builder, tree_comparator, transfer_handler
from .tree_comparator import Actions
from .tree_node import TreeNode


class DecisionEngine(Thread):
    def __init__(self, running: bool):
        Thread.__init__(self)
        self.setName("Algoritmo V2")
        self.setDaemon(True)
        self.env_settings = QSettings()
        # TODO: Il refresh minimo sarà ogni 60 secondi
        self.refresh: int = 15
        self.running = running

        self.logger = logging.getLogger("decision_engine")

    def run(self):
        # Override the run() function of Thread class
        while True:
            if self.running:
                self.compute_decision()
                sleep(max(5, self.refresh))
            else:
                sleep(5)

    def set_running(self, running: bool) -> None:
        self.running = running

    def compute_decision(self) -> None:
        path = self.env_settings.value("sync_path")
        client_tree = tree_builder.get_tree_from_system(path)
        remote_tree = tree_builder.get_tree_from_node_id()
        # self.logger.info("CLIENT")
        # self.logger.info("\n" + str(client_tree))
        # self.logger.info("SERVER")
        # self.logger.info("\n" + str(remote_tree))

        result = tree_comparator.compareFolders(client_tree, remote_tree)
        if len(result) == 0:
            self.logger.info("Nessuna azione da intraprendere")
        for r in result:
            action: Actions = r["action"]
            node: TreeNode = r["node"]
            self.logger.info(action.name + " " + node.get_name())
            if action == Actions.CLIENT_NEW_FOLDER:
                id_parent = r["id"]
                transfer_handler.upload_folder(node, id_parent)
            elif action == Actions.CLIENT_NEW_FILE:
                path = r["id"]
                transfer_handler.upload_file(node, path)
            elif action == Actions.CLIENT_UPDATE_FILE:
                path = r["id"]
                transfer_handler.upload_file(node, path)
            elif action == Actions.SERVER_NEW_FOLDER:
                path = r["path"]
                transfer_handler.download_folder(node, path)
            elif action == Actions.SERVER_NEW_FILE:
                path = r["path"]
                transfer_handler.download_file(node, path)
            elif action == Actions.SERVER_UPDATE_FILE:
                path = r["path"]
                transfer_handler.download_file(node, path)