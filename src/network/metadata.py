import os
from enum import Enum
from datetime import datetime
from network.server import Server
from typing import Dict
from PySide6.QtCore import (QSettings)


class Policy(Enum):
    Client = 1
    Server = 2
    lastUpdate = 3


class MetaData:
    def __init__(self):
        # file che son nel client e non sono nel server
        self._new_files_client: list[list[str, str]] = []
        # file che son nel server e non sono nel client
        self._new_files_server: list[list[str, str]] = []
        # file nel client che sono più aggiornati rispetto a quelli nel server
        self._update_files_client: list[list[str, str]] = []
        # file nel server che sono più aggiornati rispetto a quelli nel client
        self._update_file_server: list[list[str, str]] = []
        """percorso cartella locale"""
        env_settings = QSettings()
        self.directory: str = env_settings.value("sync_path")

        self.server: Server = Server()

        # metadata dei file nel client
        #  self.getDataClient()
        # """metadata dei file nel server"""
        # self.getDataServer()

    def get_data_server(self) -> Dict[str, str]:
        return self.server.get_all_files()

    def update_diff(self):
        self._new_files_client.clear()
        self._new_files_server.clear()
        self._update_files_client.clear()
        self._update_file_server.clear()

        file_presenti_nel_server = self.get_data_server()
        file_presenti_nel_client = self.get_data_client()
        # controllo che tutti i file del server siano uguali a quelli del client e la data di ultima modifica
        for server_file in file_presenti_nel_server:
            nome = server_file["Nome"]
            ultima_modifica = server_file["DataUltimaModifica"]
            trovato = False
            for client_file in file_presenti_nel_client:
                if nome == client_file["Nome"]:
                    if ultima_modifica != client_file["DataUltimaModifica"]:
                        if ultima_modifica > client_file["DataUltimaModifica"]:
                            print(f"{nome} è stato modificato nel server")
                            self._update_file_server.append(
                                [nome, ultima_modifica])
                        else:
                            print(f"{nome} è stato modificato nel client")
                            self._update_files_client.append(
                                [nome, client_file['DataUltimaModifica']])
                    trovato = True
                    break
            if not trovato:
                print(f"Il file {nome} non è presente nel client")
                self._new_files_server.append([nome, ultima_modifica])

        # controllo che tutti i file nel client sono uguali al quelli nel server
        for client_file in file_presenti_nel_client:
            nome = client_file["Nome"]
            ultima_modifica = client_file["DataUltimaModifica"]
            trovato = False
            for y in file_presenti_nel_server:
                if nome == y["Nome"]:
                    trovato = True
                    break
            if not trovato:
                print(f"Il file {nome} non è presente nel server")
                self._new_files_client.append([nome, ultima_modifica])

    def apply_change_server(self):
        """aggiorno il client:
             -aggiungo i nuovi file presenti nel server
             -elimino i file che non son presenti nel server
             -aggiorno nel client tutti i file che hanno DataUltimaModifica differente dal server (anche se hanno una data di ultima modifica maggiore vince il server)"""
        for i in self._new_files_server:
            """download dei file non presenti nel client"""
            # TODO
        for i in self._new_files_client:
            """rimuovo i file non presenti nel server"""
            file_path = os.path.join(self.directory, i[0])
            os.remove(file_path, i[1])
        for y in self._update_file_server:
            # devo cancellare i file nel client con nome y["nome"] e esportare dal server il file y["nome"] e caricarlo nel client
            file_path = os.path.join(self.directory, i[0])
            self.server.download_from_server(file_path, i[1])
        for y in self._update_files_client:
            # stessa cosa di sopra
            file_path = os.path.join(self.directory, i[0])
            self.server.download_from_server(file_path, i[1])

    def apply_change_client(self):
        """aggiorno il server:
            -aggiungo i nuovi file presenti nel client
            -elimino i file che non son presenti nel nel Client
            -aggiorno nel server tutti i file che hanno DataUltimaModifica differente dal client (anche se hanno una data di ultima modifica maggiore vince il client)"""
        for i in self._new_files_client:
            """aggiorno nel server i nuovi file presenti nel Client"""
            file_path = os.path.join(self.directory, i[0])
            self.server.send_to_server(file_path, i[1])
            print(f"aggiunto al server il file {i[0]}")
        for i in self._new_files_server:
            """elimino i nuovi file nel server"""
            self.server.remove_file_by_name(i[0])
        for i in self._update_files_client:
            """invio i file aggiornati nel client al server"""
            file_path = os.path.join(self.directory, i[0])
            self.server.send_to_server(file_path, i[1])
        for y in self._update_file_server:
            """ripristino i file nel server alla versione che è presente nel client"""
            for i in self.get_data_client():
                if i["Nome"] == y[0]:
                    file_path = os.path.join(self.directory, i['Nome'])
                    self.server.send_to_server(
                        file_path, i["DataUltimaModifica"])
                    break

    def apply_change_last_update(self) -> None:
        """sincronizzo i nuovi file
           aggiungo nel server solo i file che nel client hanno l ultima modifica maggiore
           aggiorno nel client i file che nel server hanno ultima modifica maggiore"""
        for i in self._new_files_client:
            """upload i file client che non sono presenti nel server"""
            file_path = os.path.join(self.directory, i[0])
            self.server.send_to_server(file_path, i[1])

        for i in self._new_files_server:
            """scarico i file che non sono presenti nel client"""
            self.server.download_from_server(i[0])
        for i in self._update_files_client:
            """aggiorno il file nel server"""
            file_path = os.path.join(self.directory, i[0])
            self.server.send_to_server(file_path, i[1])
        for i in self._update_file_server:
            """aggiorno i file nel client"""
            self.server.download_from_server(i[0])

    def apply_changes(self, policy: Policy) -> None:
        self.update_diff()
        if policy == Policy.Client:
            self.apply_change_client()
        elif policy == Policy.Server:
            self.apply_change_server()
        elif Policy.lastUpdate:
            self.apply_change_last_update()
        else:
            print("Invalid policy")

    def metadata(self, file: str) -> dict:
        name = os.path.basename(file)
        size = os.path.getsize(file)
        ultima_modifica = datetime.fromtimestamp(
            os.stat(file).st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        data = {
            'Nome': name,
            'Dimensione': size,
            'DataUltimaModifica': ultima_modifica
        }
        print(f"Nome: {name} data ultima modifica: {ultima_modifica}")
        return data

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
        # with open("file.json", "w") as outfile:
        #    json.dump(data, outfile, indent=4)
        return data


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
