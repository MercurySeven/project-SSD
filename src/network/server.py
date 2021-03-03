import base64
import os
import time
import datetime
import settings
import logging
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from typing import Dict
from PySide6.QtCore import (QSettings)


class Server:

    def __init__(self):
        self.url: str = settings.get_server_url()
        self.env_settings = QSettings()

        transport = AIOHTTPTransport(url=self.url)
        self.client: Client = Client(transport=transport)
        self.logger = logging.getLogger("server")

    def send_to_server(self, file_path: str, last_update: str) -> None:
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

        with open(file_path, "rb") as f:
            params = {
                "file": f,
                "datetime": last_update
            }

            self.client.execute(
                query, variable_values=params, upload_files=True
            )

            self.logger.info(
                f"Inviato al server il file {file_path} ultimo aggiornamento {last_update}")

    def download_from_server(self, file_name: str) -> None:
        """
            Scarica il file dal server e lo salva nel path, filename deve
            comprendere anche l'estensione
        """
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
            "fileName": file_name
        }
        response = self.client.execute(query, variable_values=params)
        base64_string = response["DownloadFile"]["Base64"]
        data_ultima_modifica = response["DownloadFile"]["DataUltimaModifica"]

        if base64_string != "-1":
            base64_bytes = base64_string.encode('ascii')

            path = os.path.join(
                self.env_settings.value("sync_path"), file_name)

            with open(path, "wb") as fh:
                fh.write(base64.decodebytes(base64_bytes))

            last_update = time.mktime(datetime.datetime.strptime(
                data_ultima_modifica, "%Y-%m-%d %H:%M:%S").timetuple())

            os.utime(path, (last_update, last_update))
            self.logger.info(
                f"File scaricato: {file_name} ultimo aggiornamento {data_ultima_modifica}")
        else:
            self.logger.warning(f"Errore nel download: {file_name}")

    def get_all_files(self) -> Dict[str, str]:
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
        self.logger.info(
            f"Richiesta di tutti i file presenti nel server: {len(response)} files")
        # result: dict[str, str] = {}
        # for items in response:
        #    result[items["Nome"]] = items["DataUltimaModifica"]

        return response

    def remove_file_by_name(self, file_name: str) -> None:
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
            "fileName": file_name
        }

        self.client.execute(query, variable_values=params)

        self.logger.info(f"Rimosso dal server il file: {file_name}")
