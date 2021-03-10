import os
import logging
from enum import Enum
from datetime import datetime
from .api import API
from typing import Dict


class Policy(Enum):
    Client = 1
    Server = 2
    lastUpdate = 3


class MetaData:
    def __init__(self, path: str):
        # file che son nel client e non sono nel server
        self._new_files_client: list[list[str]] = []
        # file che son nel server e non sono nel client
        self._new_files_server: list[list[str]] = []
        # file nel client che sono più aggiornati rispetto a quelli nel server
        self._update_files_client: list[list[str]] = []
        # file nel server che sono più aggiornati rispetto a quelli nel client
        self._update_file_server: list[list[str]] = []
        """percorso cartella locale"""
        self.directory = path

        self._politica: Policy = Policy.lastUpdate
        # TODO: Da sistemare non appena finiamo il refactor
        self._api = API("***", "***")
        self._logger = logging.getLogger("metadata")

    def setDirectory(self, path: str):
        self.directory = path

    def get_data_server(self) -> Dict[str, str]:
        return self._api.get_all_files()

    def get_data_client(self) -> list:
        p = []
        for root, dirs, files in os.walk(self.directory):
            for name in files:
                if dir == root:
                    p.append(f"{root}{name}")
                else:
                    p.append(os.path.join(root, name))
        data = []
        for file in p:
            data.append(self.metadata(file))
        return data

    def metadata(self, file: str) -> dict:
        name = os.path.basename(file)
        size = os.path.getsize(file)
        updated_at = datetime.fromtimestamp(
            os.stat(file).st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        data = {
            'name': name,
            'size': size,
            'updated_at': updated_at
        }
        self._logger.info(
            f"Nome: {name} data ultima modifica: {updated_at}")
        return data

    def update_diff(self):
        self._new_files_client.clear()
        self._new_files_server.clear()
        self._update_files_client.clear()
        self._update_file_server.clear()

        file_presenti_nel_server = self.get_data_server()
        file_presenti_nel_client = self.get_data_client()
        # controllo che tutti i file del server siano uguali a quelli del
        # client e la data di ultima modifica
        for server_file in file_presenti_nel_server:
            name = server_file["name"]
            updated_at = server_file["updated_at"]
            id = server_file["id"]
            trovato = False
            for client_file in file_presenti_nel_client:
                if name == client_file["name"]:
                    if updated_at != client_file["updated_at"]:
                        if updated_at > client_file["updated_at"]:
                            self._logger.info(
                                f"{name} è stato modificato nel server")
                            self._update_file_server.append(
                                [name, updated_at, id])
                        else:
                            self._logger.info(
                                f"{name} è stato modificato nel client")
                            self._update_files_client.append(
                                [name, client_file['updated_at'], id])
                    trovato = True
                    break
            if not trovato:
                self._logger.info(f"Il file {name} non è presente nel client")
                self._new_files_server.append([name, updated_at, id])

        # controllo che tutti i file nel client
        # sono uguali al quelli nel server
        for client_file in file_presenti_nel_client:
            name = client_file["name"]
            updated_at = client_file["updated_at"]
            trovato = False
            for y in file_presenti_nel_server:
                if name == y["name"]:
                    trovato = True
                    break
            if not trovato:
                self._logger.info(f"Il file {name} non è presente nel server")
                self._new_files_client.append([name, updated_at])

    def apply_change_server(self):
        """aggiorno il client:
             -aggiungo i nuovi file presenti nel server
             -elimino i file che non son presenti nel server
             -aggiorno nel client tutti i file che hanno DataUltimaModifica
                differente dal server (anche se hanno una data di
                ultima modifica maggiore vince il server)"""
        for name, updated_at, id in self._update_file_server:
            # devo cancellare i file nel client con nome y["nome"] e esportare
            # dal server il file y["nome"] e caricarlo nel client
            self._api.download_from_server(self.directory, name, id)
        for name, updated_at, id in self._update_files_client:
            # stessa cosa di sopra
            self._api.download_from_server(self.directory, name, id)

    def apply_change_client(self):
        """aggiorno il server:
            -aggiungo i nuovi file presenti nel client
            -elimino i file che non son presenti nel nel Client
            -aggiorno nel server tutti i file che hanno DataUltimaModifica
               differente dal client (anche se hanno una data di ultima
               modifica maggiore vince il client)"""

        for name, _ in self._update_files_client:
            """invio i file aggiornati nel client al server"""
            file_path = os.path.join(self.directory, name)
            self._api.upload_to_server(file_path)
        for name, updated_at, id in self._update_file_server:
            """ripristino i file nel server alla versione che è presente nel client"""
            for i in self.get_data_client():
                if i["name"] == name:
                    file_path = os.path.join(self.directory, name)
                    self._api.upload_to_server(file_path)
                    break

    def apply_change_last_update(self) -> None:
        """sincronizzo i nuovi file
           aggiungo nel server solo i file che nel client hanno l'ultima modifica maggiore
           aggiorno nel client i file che nel server hanno ultima modifica maggiore"""
        for name, updated_at, id in self._update_files_client:
            """aggiorno il file nel server"""
            file_path = os.path.join(self.directory, name)
            self._api.upload_to_server(file_path)
        for name, updated_at, id in self._update_file_server:
            """aggiorno i file nel client"""
            self._api.download_from_server(self.directory, name, id)

    def default_operations(self) -> None:
        """Scarico i file che non sono presenti nel client
           Carico i file che non sono presenti nel server"""
        for name, _ in self._new_files_client:
            """upload i file che non sono presenti nel server"""
            file_path = os.path.join(self.directory, name)
            self._api.upload_to_server(file_path)
        for name, updated_at, id in self._new_files_server:
            """download i file che non sono presenti nel client"""
            self._api.download_from_server(self.directory, name, id)

    def change_policy(self, policy):
        self._politica = policy
        self._logger.info(f"modificato politica {self._politica}")

    def apply_changes(self) -> None:
        self.update_diff()
        self.default_operations()
        if self._politica == Policy.Client:
            self.apply_change_client()
        elif self._politica == Policy.Server:
            self.apply_change_server()
        elif self._politica == Policy.lastUpdate:
            self.apply_change_last_update()
        else:
            self._logger.info("Invalid policy")

    def get_size(self) -> int:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size


"""
print(f"file presenti nel client {metadata.getDataClient()}")
print(f"file presenti nel server {metadata.getDataServer()}")
metadata.updateDiff()
print(f"nuovi file nel server {metadata.newFilesServer}")
print(f"nuovi file nel client {metadata.newFilesClient}")
print(f"file aggiornati nel client {metadata.updateFilesClient}")
print(f"file aggiornati nel client {metadata.updateFileServer}")
server = Server()
metadata.applyChanges(Policy.lastUpdate)

for i in metadata.getDataServer():
    server.removeFileByName(f"{i['Nome']}")
"""
