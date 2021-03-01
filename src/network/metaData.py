from enum import Enum
import os
from datetime import datetime
from server import Server
from settings import Settings


class Policy(Enum):
    Client = 1
    Server = 2
    lastUpdate = 3


class metaData:
    def __init__(self):
        # file che son nel client e non sono nel server
        self.newFilesClient = []
        # file che son nel server e non sono nel client
        self.newFilesServer = []
        # file nel client che sono più aggiornati rispetto a quelli nel server
        self.updateFilesClient = []
        # file nel server che sono più aggiornati rispetto a quelli nel client
        self.updateFileServer = []
        """percorso cartella locale"""
        settings = Settings()
        self.directory = settings.get_path()
        # self.directory = "C:\\Users\Poppi\Desktop\LOCAL"
        # metadata dei file nel client
        self.metaClient = self.getDataClient()
        """metadata dei file nel server"""
        self.metaServer = self.getDataServer()

    def getDataServer(self):
        server = Server()
        return server.getAllFiles()

    def updateDiff(self):
        # controllo che tutti i file del server siano uguali a quelli del client e la data di ultima modifica
        for i in self.getDataServer():
            nome = i["Nome"]
            ultimaModifica = i["DataUltimaModifica"]
            trovato = False
            for y in self.getDataClient():
                if i["Nome"] == y["Nome"]:
                    if i["DataUltimaModifica"] != y["DataUltimaModifica"]:
                        if i["DataUltimaModifica"] > y["DataUltimaModifica"]:
                            print(f"{nome} è stato modificato nel server")
                            self.updateFileServer.append([nome, ultimaModifica])
                        else:
                            print(f"{nome} è stato modificato nel client")
                            self.updateFilesClient.append([nome, y['DataUltimaModifica']])
                    trovato = True
                    break
            if not trovato:
                print(f"Il file {nome} non è presente nel client")
                self.newFilesServer.append([nome, ultimaModifica])

        # controllo che tutti i file nel client sono uguali al quelli nel server
        for i in self.getDataClient():
            nome = i["Nome"]
            ultimaModifica = i["DataUltimaModifica"]
            trovato = False
            for y in self.getDataServer():
                if i["Nome"] == y["Nome"]:
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
        server = Server()
        for i in self.newFilesServer:
            """aggiungo nel client i nuovi file presenti nel server"""
            # TODO
        for i in self.newFilesClient:
            """rimuovo i nuovi file del client"""
            print(f"rimosso il file {self.directory}\\{i[0]}")
            # os.remove(f"{self.directory}\\{i[0]}")
            # TODO
        for y in self.updateFileServer:
            # devo cancellare i file nel client con nome y["nome"] e esportare dal server il file y["nome"] e caricarlo nel client
            # TODO
            ''
        for y in self.updateFilesClient:
            # stessa cosa di sopra
            # TODO
            ''

    def applyChangeClient(self):
        """aggiorno il server:
            -aggiungo i nuovi file presenti nel client
            -elimino i file che non son presenti nel nel Client
            -aggiorno nel server tutti i file che hanno DataUltimaModifica differente dal client (anche se hanno una data di ultima modifica maggiore vince il client)"""
        server = Server()
        for i in self.newFilesClient:
            """aggiorno nel server i meta dei nuovi file"""
            server.sendToServer(f"{self.directory}\\{i[0]}", i[1])
            print(f"aggiunto metadati al server del file {i[0]}")
            """aggiungo file"""
            # TODO
        for i in self.newFilesServer:
            """elimino i metadati dei nuovi file nel server"""
            server.removeFileByName(i[0])
            """elimino i file dal server """
            # TODO
        for i in self.updateFilesClient:
            """aggiorno i metadata dei file aggiornati nel client al server"""
            server.sendToServer(f"{self.directory}\\{i[0]}", i[1])
            """invio il file aggiornato al server"""
            # TODO
        for y in self.updateFileServer:
            """ripristino i metadati alla versione che è presente nel client"""
            for i in self.getDataClient():
                if i["Nome"] == y[0]:
                    server.sendToServer(f"{self.directory}\\{i['Nome']}", i["DataUltimaModifica"])
                    """ invio il file i["nome"] al server"""
                    # TODO
                    break

    def applyChangeLastUpdate(self):
        """sincronizzo i nuovi file (problema sul controllo dei nomi)
           aggiungo nel server solo i file che nel client hanno l ultima modifica maggiore
           aggiorno nel client i file che nel server hanno ultima modifica superiore"""
        server: Server = Server()
        for i in self.newFilesClient:
            server.sendToServer(f"{self.directory}\\{i[0]}", i[1])
            """inserisco il nuovo file nel server"""
            # TODO
        for i in self.newFilesServer:
            """inserisco il nuovo file y[0] nel client"""
            # TODO
        for i in self.updateFilesClient:
            """aggiorno il file nel server"""
            # TODO
            """aggiorno i metadati nel server"""
            server.sendToServer(f"{self.directory}\\{i[0]}", i[1])
        for i in self.updateFileServer:
            """aggiorno i file nel client"""
            # TODO

    def applyChanges(self, policy: Policy):
        self.updateDiff()
        if policy == Policy.Client:
            self.applyChangeClient()
        elif policy == Policy.Server:
            self.applyChangeServer()
        elif Policy.lastUpdate:
            self.applyChangeLastUpdate()
        else:
            print("Invalid policy")

    def metadata(self, file: str):
        name = os.path.basename(file)
        size = os.path.getsize(file)
        ultima_modifica = datetime.fromtimestamp(os.stat(file).st_mtime).strftime("%Y-%m-%d %I:%M:%S")
        data = {
            'Nome': name,
            'Dimensione': size,
            'DataUltimaModifica': ultima_modifica
        }
        return data

    def getDataClient(self):
        p = []
        for root, dirs, files in os.walk(self.directory):
            for name in files:
                if dir == root:
                    p.append(f"{root}{name}")
                else:
                    p.append(f"{root}\\{name}")
        data = []
        for file in p:
            data.append(self.metadata(file))
        # with open("file.json", "w") as outfile:
        #    json.dump(data, outfile, indent=4)
        return data


metadata = metaData()
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