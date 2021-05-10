from PySide2.QtWidgets import (QApplication, QSystemTrayIcon)
from src.view.notification_view import NotificationView
from src.view.main_view import MainWindow
from src.algorithm.tree_comparator import Actions


class NotificationController:

    def __init__(self, app: QApplication, view: MainWindow):
        self.notification_view = NotificationView(app)

        self.notification_view.exit_option.triggered.connect(app.quit)
        self.notification_view.show_option.triggered.connect(view.show)

        self.notification_view.show()

        self.server_update_file: int = 0
        self.server_update_file_message: str = ""
        self.server_new_file: int = 0
        self.server_new_file_message: str = ""

        self.network_error: int = 0
        self.network_message: str = ""
        self.space_error: int = 0
        self.space_message: str = ""

    def send_message(self,
                     msg: str,
                     duration: int = 2000,
                     icon: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.Information) -> None:
        self.notification_view.show_message("SSD: Zextras Drive Desktop", msg, duration, icon)

    def send_best_message(self, duration: int = 2000) -> None:
        """
            Ordine di priorità notifiche
            1. Errore di rete durante il download
            2. Spazio non disponibile
            3. Sono stati aggiornati 1+ file
            4. È stato aggiornato 1 file
            5. Sono stati scaricati 1+ file
            6. È stato scaricato 1 file
        """

        if self.network_error > 0:
            self.send_message(self.network_message, duration, QSystemTrayIcon.Warning)
        elif self.space_error > 0:
            self.send_message(self.space_message, duration, QSystemTrayIcon.Warning)
        elif self.server_update_file > 0:
            self.send_message(self.server_update_file_message, duration)
        elif self.server_new_file > 0:
            self.send_message(self.server_new_file_message, duration)

        # Una volta inviato il messaggio resettiamo i contatori
        self._reset()

    def add_notification(self, node_message: dict) -> None:
        if node_message["result"]:
            if node_message["action"] == Actions.SERVER_UPDATE_FILE:
                self._add_server_update_file(node_message["node_name"])
            elif node_message["action"] == Actions.SERVER_NEW_FILE:
                self._add_server_new_file(node_message["node_name"])
        else:
            # Messaggio di errore
            if node_message["type"] == "network_error":
                self._add_network_error(node_message["node_name"])
            elif node_message["type"] == "space_error":
                self._add_space_error(node_message["node_name"])

    def _add_server_update_file(self, node_name: str) -> None:
        self.server_update_file += 1
        msg = ""
        if self.server_update_file == 1:
            msg = f"È stato aggiornato {node_name}"
        else:
            msg = f"Sono stati aggiornati {self.server_update_file} files"
        self.server_update_file_message = msg

    def _add_server_new_file(self, node_name: str) -> None:
        self.server_new_file += 1
        msg = ""
        if self.server_new_file == 1:
            msg = f"È stato scaricato {node_name}"
        else:
            msg = f"Sono stati scaricati {self.server_new_file} files"
        self.server_new_file_message = msg

    def _add_network_error(self, node_name: str) -> None:
        self.network_error += 1
        msg = ""
        if self.network_error == 1:
            msg = f"Errore di rete mentre scaricavo il file {node_name}"
        else:
            msg = "Errore di rete mentre scaricavo i files"
        self.network_message = msg

    def _add_space_error(self, node_name: str) -> None:
        self.space_error += 1
        msg = ""
        if self.space_error == 1:
            msg = f"Spazio non disponibile per scaricare il file {node_name}"
        else:
            msg = "Non hai abbastanza spazio per scaricare i files"
        self.space_message = msg

    def _reset(self) -> None:
        self.server_update_file = 0
        self.server_update_file_message = ""
        self.server_new_file = 0
        self.server_new_file_message = ""

        self.network_error = 0
        self.network_message = ""
        self.space_error = 0
        self.space_message = ""
