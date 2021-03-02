from enum import Enum
import os
from datetime import datetime
from network.server import Server
from settings import Settings
from typing import Dict


class Policy(Enum):
    Client = 1
    Server = 2
    lastUpdate = 3


class metaData:
    def __init__(self):
        # file che son nel client e non sono nel server
        self.newFilesClient: list[list[str, str]] = []
        # file che son nel server e non sono nel client
        self.newFilesServer: list[list[str, str]] = []
        # file nel client che sono più aggiornati rispetto a quelli nel server
        self.updateFilesClient: list[list[str, str]] = []
        # file nel server che sono più aggiornati rispetto a quelli nel client
        self.updateFileServer: list[list[str, str]] = []
        """percorso cartella locale"""
        settings = Settings()
        self.directory: str = settings.get_path()

        self.server: Server = Server()

        # metadata dei file nel client
        #  self.getDataClient()
        # """metadata dei file nel server"""
        # self.getDataServer()

    def getDataServer(self) -> Dict[str, str]:
        return self.server.getAllFiles()

    def updateDiff(self):
        self.newFilesClient = []
        self.newFilesClient = []
        self.updateFilesClient = []
        self.updateFileServer = []
        # controllo che tutti i file del server siano uguali a quelli del client e la data di ultima modifica
        for server_file in self.getDataServer():
            nome = server_file["Nome"]
            ultimaModifica = server_file["DataUltimaModifica"]
            trovato = False
            for client_file in self.getDataClient():
                if nome == client_file["Nome"]:
                    if ultimaModifica != client_file["DataUltimaModifica"]:
                        if ultimaModifica > client_file["DataUltimaModifica"]:
                            print(f"{nome} è stato modificato nel server")
                            self.updateFileServer.append(
                                [nome, ultimaModifica])
                        else:
                            print(f"{nome} è stato modificato nel client")
                            self.updateFilesClient.append(
                                [nome, client_file['DataUltimaModifica']])
                    trovato = True
                    break
            if not trovato:
                print(f"Il file {nome} non è presente nel client")
                self.newFilesServer.append([nome, ultimaModifica])

        # controllo che tutti i file nel client sono uguali al quelli nel server
        for client_file in self.getDataClient():
            nome = client_file["Nome"]
            ultimaModifica = client_file["DataUltimaModifica"]
            trovato = False
            for y in self.getDataServer():
                if nome == y["Nome"]:
                    trovato = True
                    break
            if not trovato:
                print(f"Il file {nome} non è presente nel server")
                self.newFilesClient.append([nome, ultimaModifica])

    def applyChangeServer(self):
        """aggiorno il client:
             -aggiungo i nuovi file presenti nel server
             -elimino i file che non son presenti nel server
             -aggiorno nel client tutti i file che hanno DataUltimaModifica differente dal server (anche se hanno una data di ultima modifica maggiore vince il server)"""
        for i in self.newFilesServer:
            """download dei file non presenti nel client"""
            # TODO
        for i in self.newFilesClient:
            """rimuovo i file non presenti nel server"""
            file_path = os.path.join(self.directory, i[0])
            os.remove(file_path, i[1])
        for y in self.updateFileServer:
            # devo cancellare i file nel client con nome y["nome"] e esportare dal server il file y["nome"] e caricarlo nel client
            file_path = os.path.join(self.directory, i[0])
            self.server.downloadFromServer(file_path, i[1])
        for y in self.updateFilesClient:
            # stessa cosa di sopra
            file_path = os.path.join(self.directory, i[0])
            self.server.downloadFromServer(file_path, i[1])

    def applyChangeClient(self):
        """aggiorno il server:
            -aggiungo i nuovi file presenti nel client
            -elimino i file che non son presenti nel nel Client
            -aggiorno nel server tutti i file che hanno DataUltimaModifica differente dal client (anche se hanno una data di ultima modifica maggiore vince il client)"""
        for i in self.newFilesClient:
            """aggiorno nel server i nuovi file presenti nel Client"""
            file_path = os.path.join(self.directory, i[0])
            self.server.sendToServer(file_path, i[1])
            print(f"aggiunto al server il file {i[0]}")
        for i in self.newFilesServer:
            """elimino i nuovi file nel server"""
            self.server.removeFileByName(i[0])
        for i in self.updateFilesClient:
            """invio i file aggiornati nel client al server"""
            file_path = os.path.join(self.directory, i[0])
            self.server.sendToServer(file_path, i[1])
        for y in self.updateFileServer:
            """ripristino i file nel server alla versione che è presente nel client"""
            for i in self.getDataClient():
                if i["Nome"] == y[0]:
                    file_path = os.path.join(self.directory, i['Nome'])
                    self.server.sendToServer(
                        file_path, i["DataUltimaModifica"])
                    break

    def applyChangeLastUpdate(self) -> None:
        """sincronizzo i nuovi file
           aggiungo nel server solo i file che nel client hanno l ultima modifica maggiore
           aggiorno nel client i file che nel server hanno ultima modifica maggiore"""
        for i in self.newFilesClient:
            """upload i file client che non sono presenti nel server"""
            file_path = os.path.join(self.directory, i[0])
            self.server.sendToServer(file_path, i[1])

        for i in self.newFilesServer:
            """scarico i file che non sono presenti nel client"""
            self.server.downloadFromServer(i[0])
        for i in self.updateFilesClient:
            """aggiorno il file nel server"""
            file_path = os.path.join(self.directory, i[0])
            self.server.sendToServer(file_path, i[1])
        for i in self.updateFileServer:
            """aggiorno i file nel client"""
            self.server.downloadFromServer(i[0])

    def applyChanges(self, policy: Policy) -> None:
        self.updateDiff()
        if policy == Policy.Client:
            self.applyChangeClient()
        elif policy == Policy.Server:
            self.applyChangeServer()
        elif Policy.lastUpdate:
            self.applyChangeLastUpdate()
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
        print("->>>>>>>>>>>>>>>>>>>>Data ultima modifica: " + ultima_modifica)
        return data

    def getDataClient(self) -> list:
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
