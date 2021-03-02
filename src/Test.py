from network.metaData import metaData, Policy
from network.server import Server
import os
import unittest
from settings import Settings


class Test(unittest.TestCase):

    def test_uno(self):
        """controllo l'inserimento di un file e l'eliminazione (politica Client)"""
        metadata = metaData()
        # server = Server()
        file_path = os.path.join(metadata.directory, "file_uno.txt")
        file_uno = open(file_path, "w")
        file_uno.close()
        metadata.applyChanges(Policy.Client)
        for i in metadata.getDataServer():
            trovato = False
            data = False
            for y in metadata.getDataClient():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    if i['DataUltimaModifica'] == y['DataUltimaModifica']:
                        data = True
                    break
            self.assertTrue(trovato)
            self.assertTrue(data)
        os.remove(file_path)
        metadata.applyChanges(Policy.Client)
        nome = "file_uno.txt"
        trovato = False
        for i in metadata.getDataServer():
            if i['Nome'] == nome:
                trovato = True
                break
        self.assertFalse(trovato)

    def test_updateFile(self):
        """controllo l'aggiornamento di un file nel client (politica Client)"""
        metadata = metaData()
        # server = Server()
        file_path = os.path.join(metadata.directory, "file_uno.txt")
        file_uno = open(file_path, "w")
        file_uno.close()
        metadata.applyChanges(Policy.Client)
        for i in metadata.getDataServer():
            trovato = False
            data = False
            for y in metadata.getDataClient():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    if i['DataUltimaModifica'] == y['DataUltimaModifica']:
                        data = True
                    break
            self.assertTrue(trovato)
            self.assertTrue(data)
        file_uno = open(file_path, "a")
        file_uno.write("nuova riga")
        file_uno.close()
        metadata.applyChanges(Policy.Client)
        for i in metadata.getDataServer():
            trovato = False
            data = False
            for y in metadata.getDataClient():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    if i['DataUltimaModifica'] == y['DataUltimaModifica']:
                        data = True
                    break
            self.assertTrue(trovato)
            self.assertTrue(data)
        os.remove(file_path)
        metadata.applyChanges(Policy.Client)
        nome = "file_uno.txt"
        trovato = False
        for i in metadata.getDataServer():
            if i['Nome'] == nome:
                trovato = True
                break
        self.assertFalse(trovato)

    def test_due(self):
        """controllo last Update"""
        metadata = metaData()
        # server = Server()
        file_path1 = os.path.join(metadata.directory, "file_uno.txt")
        file_uno = open(file_path1, "w")
        file_uno.close()
        file_path2 = os.path.join(metadata.directory, "file_due.txt")
        file_due = open(file_path2, 'w')
        file_due.close()
        metadata.applyChanges(Policy.lastUpdate)
        for i in metadata.getDataServer():
            trovato = False
            for y in metadata.getDataClient():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    break
            self.assertTrue(trovato)
        for i in metadata.getDataClient():
            trovato = False
            for y in metadata.getDataServer():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    break
            self.assertTrue(trovato)
        os.remove(file_path2)
        file_path3 = os.path.join(metadata.directory, "file_tre.txt")
        file_tre = open(file_path3, 'w')
        file_tre.close()
        metadata.applyChanges(Policy.lastUpdate)
        for i in metadata.getDataServer():
            trovato = False
            for y in metadata.getDataClient():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    break
            self.assertTrue(trovato)
        for i in metadata.getDataClient():
            trovato = False
            for y in metadata.getDataServer():
                if i['Nome'] == y['Nome']:
                    trovato = True
                    break
            self.assertTrue(trovato)
        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)
        metadata.applyChanges(Policy.Client)
        nome = "file_uno.txt"
        trovato = False
        for i in metadata.getDataServer():
            if i['Nome'] == nome:
                trovato = True
                break
        self.assertFalse(trovato)
        nome = "file_due.txt"
        trovato = False
        for i in metadata.getDataServer():
            if i['Nome'] == nome:
                trovato = True
                break
        self.assertFalse(trovato)
        nome = "file_tre.txt"
        trovato = False
        for i in metadata.getDataServer():
            if i['Nome'] == nome:
                trovato = True
                break
        self.assertFalse(trovato)
