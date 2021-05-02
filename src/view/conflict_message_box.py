from PySide6.QtWidgets import (QMessageBox)
from PySide6.QtCore import (Slot)

from src.model.algorithm.node import Node


class ConflictMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSD: Risolvi il conflitto")
        self.setText("Il documento è stato modificato anche nel server")
        # self.setInformativeText(
        #     "Dato che hai scelto la politica manuale, puoi decidere che file tenere")
        self.setIcon(QMessageBox.Question)

        self.keep_client_button = self.addButton(
            "Tieni la tua versione", QMessageBox.ButtonRole.AcceptRole)
        self.keep_server_button = self.addButton(
            "Tieni la versione del server", QMessageBox.ButtonRole.RejectRole)

    @Slot(Node, Node)
    def set_info(self, client: Node, server: Node) -> None:
        text = ("Dato che hai scelto la politica manuale, puoi decidere che file tenere:\n"
                "<table><thead><tr><th></th><th>Client</th><th>Server</th></tr></thead>"
                f"<tbody><tr><td>Nome</td><td>{client.name}</td><td>{server.name}</td></tr>"
                "<tr><td>Ultima modifica</td>"
                f"<td>{client.updated_at}</td><td>{server.updated_at}</td></tr>"
                f"<td>Last editor</td><td>Tu</td><td>{server.last_editor}</td></tr>"
                "</tbody></table>")

        self.setInformativeText(text)
        self.exec_()
