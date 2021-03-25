from threading import Thread
from time import sleep
import logging
import os
import shutil

from PySide6.QtCore import QSettings

from . import tree_builder, tree_comparator, transfer_handler, compare_client_snapshot as ccs
from .tree_comparator import Actions
from src.model.network.tree_node import TreeNode


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
                path = self.env_settings.value("sync_path")
                snap_tree = tree_builder.read_dump_client_filesystem(path)
                client_tree = tree_builder.get_tree_from_system(path)

                ccs.compare_snap_client(snap_tree, client_tree)
                remote_tree = tree_builder.get_tree_from_node_id()
                self.compute_decision(client_tree, remote_tree)
                self.logger.info("Eseguito DUMP dell'albero locale")
                tree_builder.dump_client_filesystem(path)
                sleep(max(5, self.refresh))
            else:
                sleep(5)

    def set_running(self, running: bool) -> None:
        self.running = running

    def compute_decision(self, client_tree: TreeNode, remote_tree: TreeNode) -> None:
        # print("CLIENT")
        # print("\n" + str(client_tree))
        # print("SERVER")
        # print("\n" + str(remote_tree))

        result = tree_comparator.compareFolders(client_tree, remote_tree)
        if len(result) == 0:
            self.logger.info("Nessuna azione da intraprendere")
        for r in result:
            action: Actions = r["action"]
            node: TreeNode = r["node"]
            name_node = node.get_name()
            self.logger.info(action.name + " " + node.get_name())
            if action == Actions.CLIENT_NEW_FOLDER:
                shutil.rmtree(node._payload.path)
                self.logger.info(f"Eliminata cartella non presente nel server: {name_node}")
            elif action == Actions.CLIENT_NEW_FILE:
                os.remove(node._payload.path)
                self.logger.info(f"Eliminato file non presente nel server: {name_node}")
            elif action == Actions.CLIENT_UPDATE_FILE:
                path = r["id"]
                transfer_handler.upload_file(node, path)
                self.logger.info(action.name + " " + name_node)
            elif action == Actions.SERVER_NEW_FOLDER:
                path = r["path"]
                transfer_handler.download_folder(node, path)
                self.logger.info(action.name + " " + name_node)
            elif action == Actions.SERVER_NEW_FILE:
                path = r["path"]
                transfer_handler.download_file(node, path)
                self.logger.info(action.name + " " + name_node)
            elif action == Actions.SERVER_UPDATE_FILE:
                path = r["path"]
                transfer_handler.download_file(node, path)
                self.logger.info(action.name + " " + name_node)
