from network.metaData import metaData, Policy
from network.server import Server
import os
import unittest
from settings import Settings


class Test(unittest.TestCase):
    """i test devono essere eseguiti con il server vuoto """

    """controllo l'inserimento di un file e l'eliminazione"""

    def test_uno(self):
        metadata = metaData()
        server = Server()
        for i in metadata.getDataServer():
            server.removeFileByName(f"{i['Nome']}")
        file_path =os.path.join(metadata.directory, "file_uno.txt")
        file_uno = open(file_path, "w")
        file_uno.close()
        metadata.applyChanges(Policy.Client)
        self.assertEqual(metadata.getDataServer()[0]['Nome'], metadata.getDataClient()[0]['Nome'])
        os.remove(file_path)
        metadata.applyChanges(Policy.Client)
        self.assertEqual(metadata.getDataServer(), metadata.getDataClient())

    """controllo l'aggiornamento di un file nel client """

    def test_updateFile(self):
        metadata = metaData()
        server = Server()
        for i in metadata.getDataServer():
            server.removeFileByName(f"{i['Nome']}")
        file_path = os.path.join(metadata.directory, "file_uno.txt")
        file_uno = open(file_path, "w")
        file_uno.close()
        metadata.applyChanges(Policy.Client)
        self.assertEqual(metadata.getDataServer()[0]['Nome'], metadata.getDataClient()[0]['Nome'])
        file_uno = open(file_path, "a")
        file_uno.write("nuova riga")
        file_uno.close()
        metadata.applyChanges(Policy.Client)
        self.assertEqual(metadata.getDataServer()[0]['Nome'], metadata.getDataClient()[0]['Nome'])
        self.assertEqual(metadata.getDataServer()[0]['DataUltimaModifica'],
                         metadata.getDataClient()[0]['DataUltimaModifica'])
        os.remove(f"{metadata.directory}\\file_uno.txt")
        metadata.applyChanges(Policy.Client)
        self.assertEqual(metadata.getDataServer(), metadata.getDataClient())

    """controllo last Update"""
    def test_due(self):
        metadata = metaData()
        server = Server()
        metadata.directory="C:\\Users\Poppi\Desktop\LOCAL"
        for i in metadata.getDataServer():
            server.removeFileByName(f"{i['Nome']}")
        file_path1 =os.path.join(metadata.directory, "file_uno.txt")
        file_uno = open(file_path1, "w")
        file_uno.close()
        file_path2 = os.path.join(metadata.directory, "file_due.txt")
        file_due = open(file_path2,'w')
        file_due.close()
        metadata.applyChanges(Policy.lastUpdate)
        for i in metadata.getDataServer():
            trovato=False
            for y in metadata.getDataClient():
                if i['Nome']==y['Nome']:
                    trovato= True
                    break
            self.assertTrue(trovato)
        for i in metadata.getDataClient():
            trovato=False
            for y in metadata.getDataServer():
                if i['Nome']==y['Nome']:
                    trovato= True
                    break
            self.assertTrue(trovato)
        #self.assertEqual(metadata.getDataServer()[0]['Nome'], metadata.getDataClient()[0]['Nome'])
        #self.assertEqual(metadata.getDataServer()[1]['Nome'], metadata.getDataClient()[1]['Nome'])
        os.remove(file_path2)
        file_path3=os.path.join(metadata.directory, "file_tre.txt")
        file_tre= open(file_path3,'w')
        file_tre.close()
        metadata.applyChanges(Policy.lastUpdate)
        for i in metadata.getDataServer():
            trovato=False
            for y in metadata.getDataClient():
                if i['Nome']==y['Nome']:
                    trovato= True
                    break
            self.assertTrue(trovato)
        for i in metadata.getDataClient():
            trovato=False
            for y in metadata.getDataServer():
                if i['Nome']==y['Nome']:
                    trovato= True
                    break
            self.assertTrue(trovato)
        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)
        metadata.applyChanges(Policy.Client)
        self.assertEqual(metadata.getDataServer(), metadata.getDataClient())
