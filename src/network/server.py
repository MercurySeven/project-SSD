import base64
import os
import time
import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from settings import Settings
from typing import Dict


class Server:

    def __init__(self):
        self.settings = Settings()
        self.url: str = self.settings.get_server_url()

        transport = AIOHTTPTransport(url=self.url)
        self.client: Client = Client(transport=transport)

    def sendToServer(self, filePath: str, lastUpdate: str) -> None:
        """Richiede il percorso del file e l'orario di ultima modifica"""
        query = gql('''
                mutation SingleUpload($file: Upload!, $datetime: String!) {
                    singleUpload(file: $file, datetime: $datetime) {
                        filename
                        mimetype
                        encoding
                    }
                }
                ''')

        with open(filePath, "rb") as f:
            params = {
                "file": f,
                "datetime": lastUpdate
            }

            result = self.client.execute(
                query, variable_values=params, upload_files=True
            )

            print(result)

    def downloadFromServer(self, fileName: str) -> None:
        """
            Scarica il file dal server e lo salva nel path, filename deve
            comprendere anche l'estensione
        """
        print(fileName)
        query = gql('''
                query DownloadFile($fileName: String!) {
                    DownloadFile(fileName: $fileName) {
                        Nome
                        Base64
                        DataUltimaModifica
                    }
                }
                ''')
        params = {
            "fileName": fileName
        }
        response = self.client.execute(query, variable_values=params)
        base64_string = response["DownloadFile"]["Base64"]
        data_ultima_modifica = response["DownloadFile"]["DataUltimaModifica"]

        if response != "0":
            base64_bytes = base64_string.encode('ascii')

            path = os.path.join(self.settings.get_path(), fileName)

            with open(path, "wb") as fh:
                fh.write(base64.decodebytes(base64_bytes))

            last_update = time.mktime(datetime.datetime.strptime(
                data_ultima_modifica, "%Y-%m-%d %H:%M:%S").timetuple())

            os.utime(path, (last_update, last_update))

    def getAllFiles(self) -> Dict[str, str]:
        """Restituisce il nome dei file con l'ultima modifica"""
        query = gql('''
                query {
                    GetAllFiles {
                        Nome
                        DataUltimaModifica
                    }
                }
                ''')
        response = self.client.execute(query)["GetAllFiles"]
        # result: dict[str, str] = {}
        # for items in response:
        #    result[items["Nome"]] = items["DataUltimaModifica"]

        return response

    def removeFileByName(self, fileName: str) -> None:
        """Rimuove il file dal cloud"""
        query = gql('''
                mutation RemoveFile($fileName: String!) {
                    removeFile(fileName: $fileName) {
                        Nome
                        DataUltimaModifica
                    }
                }
                ''')

        params = {
            "fileName": fileName
        }

        result = self.client.execute(query, variable_values=params)

        print(result)
