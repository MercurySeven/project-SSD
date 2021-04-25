import logging
import os
import shutil
from threading import Thread
from time import sleep

from PySide6.QtCore import QSettings

from src import settings
from src.model.algorithm.policy import Policy
from src.model.algorithm.tree_node import TreeNode
from src.network.api_exceptions import APIException
from . import tree_builder, tree_comparator, os_handler
from .compare_snap_client import CompareSnapClient
from .strategy.client_strategy import ClientStrategy
from .strategy.manual_strategy import ManualStrategy
from .strategy.strategy import Strategy
from .tree_comparator import Actions
from ..controllers.notification_controller import NotificationController
from ..model.main_model import MainModel


class DecisionEngine(Thread):
    def __init__(self, main_model: MainModel, notification: NotificationController, running: bool = False):
        Thread.__init__(self)

        self.setName("Algoritmo V3")
        self.setDaemon(True)
        self.env_settings = QSettings()
        # TODO: Il refresh minimo sarà ogni 60 secondi
        self.refresh: int = 15
        self.running = running

        # set istanza di NetworkModel nei moduli per poter gestire i segnali di errore
        os_handler.set_model(main_model.network_model, main_model.settings_model)
        os_handler.set_notification(notification)
        tree_builder.set_model(main_model.network_model)

        self.compare_snap_client = CompareSnapClient()
        self.strategy: dict[Policy, Strategy] = {
            Policy.Client: ClientStrategy(),
            Policy.Manual: ManualStrategy()
        }

        self.logger = logging.getLogger("decision_engine")

    def set_running(self, running: bool) -> None:
        self.running = running

    def run(self):
        # Override the run() function of Thread class
        while True:
            if self.running:
                self.check()
                sleep(max(5, self.refresh))
            else:
                sleep(5)

    def check(self) -> None:
        path = self.env_settings.value("sync_path")
        snap_tree = tree_builder.read_dump_client_filesystem(path)
        client_tree = tree_builder.get_tree_from_system(path)

        check_connection = True
        try:
            if snap_tree is not None:
                policy = Policy(settings.get_policy())
                self.compare_snap_client.check(snap_tree, client_tree, self.strategy[policy])
        except APIException:
            check_connection = False

        # Se non ho connessione mi fermo e non creo nemmeno un nuovo snapshot
        if check_connection:
            remote_tree = tree_builder.get_tree_from_node_id()
            self.compute_decision(client_tree, remote_tree, snap_tree is not None)
            self.logger.info("Eseguito snapshot dell'albero locale")
            tree_builder.dump_client_filesystem(path)

    def compute_decision(self,
                         client_tree: TreeNode,
                         remote_tree: TreeNode,
                         snapshot: bool) -> None:

        result = tree_comparator.compareFolders(client_tree, remote_tree)
        if len(result) == 0:
            self.logger.info("Nessuna azione da intraprendere")
        for r in result:
            action: Actions = r["action"]
            node: TreeNode = r["node"]
            name_node = node.get_name()
            if action == Actions.CLIENT_NEW_FOLDER:
                if snapshot:
                    shutil.rmtree(node._payload.path)
                    self.logger.info(f"Eliminata cartella non presente nel server: {name_node}")
                else:
                    id_parent = r["id"]
                    os_handler.upload_folder(node, id_parent)
                    self.logger.info(f"Nuova cartella da caricare nel server: {name_node}")
            elif action == Actions.CLIENT_NEW_FILE:
                if snapshot:
                    os.remove(node._payload.path)
                    self.logger.info(f"Eliminato file non presente nel server: {name_node}")
                else:
                    path = r["id"]
                    os_handler.upload_file(node, path)
                    self.logger.info(f"Nuovo file da caricare nel server: {name_node}")
            elif action == Actions.SERVER_NEW_FOLDER:
                path = r["path"]
                os_handler.download_folder(node, path)
                self.logger.info(action.name + " " + name_node)
            elif action == Actions.SERVER_NEW_FILE:
                path = r["path"]
                os_handler.download_file(node, path)
                self.logger.info(action.name + " " + name_node)
            elif action == Actions.SERVER_UPDATE_FILE:
                path = r["path"]
                os_handler.download_file(node, path)
                self.logger.info(action.name + " " + name_node)
