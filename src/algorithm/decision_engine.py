import logging
import os
import shutil
from threading import Thread, Condition

from PySide6.QtCore import QSettings, Slot
from PySide6.QtWidgets import (QSystemTrayIcon)

from src import settings
from src.controllers.notification_controller import NotificationController
from src.model.algorithm.policy import Policy
from src.model.algorithm.tree_node import TreeNode
from src.model.main_model import MainModel
from src.model.settings_model import SettingsModel
from src.network.api_exceptions import APIException, LoginError
from . import tree_builder, tree_comparator, os_handler
from .compare_snap_client import CompareSnapClient
from .strategy.client_strategy import ClientStrategy
from .strategy.manual_strategy import ManualStrategy
from .strategy.strategy import Strategy
from .tree_comparator import Actions


class DecisionEngine(Thread):
    def __init__(self,
                 main_model: MainModel,
                 notification_controller: NotificationController,
                 running: bool = False):
        Thread.__init__(self)

        self.setName("Algoritmo V4")
        self.setDaemon(True)
        self.env_settings = QSettings()
        self.settings_model: SettingsModel = main_model.settings_model

        self.refresh: int = (lambda: self.settings_model.get_sync_time())
        self.running = running
        self.notification_controller = notification_controller

        # set istanza di NetworkModel nei moduli per poter gestire i segnali di errore
        os_handler.set_network_model(main_model.network_model)
        os_handler.set_settings_model(main_model.settings_model)
        tree_builder.set_model(main_model.network_model)

        self.main_model = main_model

        self.compare_snap_client = CompareSnapClient()
        self.strategy: dict[Policy, Strategy] = {
            Policy.Client: ClientStrategy(),
            Policy.Manual: ManualStrategy()
        }

        self.logger = logging.getLogger("decision_engine")
        self.condition = Condition()

    def set_running(self, running: bool) -> None:
        self.running = running

    def run(self):
        # Override the run() function of Thread class
        while True:
            self.condition.acquire()
            if self.running:
                self.check()
                self.condition.wait(max(5, self.refresh()))
            else:
                self.condition.wait(5)
            self.condition.release()

    @Slot()
    def Sl_model_changed(self):
        self.condition.acquire()
        try:
            self.condition.notify()
        finally:
            self.condition.release()

    def check(self) -> None:
        self.logger.info("Avvio sincronizzazione")
        path = self.env_settings.value("sync_path")
        if not os.path.isdir(path):
            self.notification_controller.send_message("La cartella scelta non è stata trovata",
                                                      icon=QSystemTrayIcon.Critical)
            self.main_model.sync_model.set_state(False)
            return
        snap_tree = tree_builder.read_dump_client_filesystem(path)
        client_tree = tree_builder.get_tree_from_system(path)

        try:
            if snap_tree is not None:
                policy = Policy(settings.get_policy())
                done_something = self.compare_snap_client.check(
                    snap_tree, client_tree, self.strategy[policy])
                if done_something:
                    client_tree = tree_builder.get_tree_from_system(path)

            remote_tree = tree_builder.get_tree_from_node_id()
            self.compute_decision(client_tree, remote_tree, snap_tree is not None)
            tree_builder.dump_client_filesystem(path)
            self.logger.info("Eseguito snapshot dell'albero locale")
            self.notification_controller.send_best_message()
        except APIException as e:
            if isinstance(e, LoginError):
                self.notification_controller.send_message(
                    "Credenziali errate. Eseguire logout e riprovare",
                    icon=QSystemTrayIcon.Critical)
                self.main_model.sync_model.set_state(False)
            else:
                self.notification_controller.send_message(
                    "Errore di connessione al drive Zextras", icon=QSystemTrayIcon.Warning)

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
                node_message = os_handler.download_folder(node, path)
                for item in node_message:
                    item["action"] = Actions.SERVER_NEW_FILE
                    self.notification_controller.add_notification(item)
                if len(node_message) > 0:
                    self.logger.info(action.name + " " + name_node)
            elif action == Actions.SERVER_NEW_FILE or action == Actions.SERVER_UPDATE_FILE:
                path = r["path"]
                node_message = os_handler.download_file(node, path)
                if node_message is not None:
                    node_message["action"] = action
                    self.notification_controller.add_notification(node_message)
                    self.logger.info(action.name + " " + name_node)
