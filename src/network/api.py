import os
import logging
import requests
import math
from .query_model import Query
from .cookie_session import CookieSession
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from PySide6.QtCore import (QSettings)


class API:

    # TODO: Da iniziare a scrive i test prima che diventi grande

    def __init__(self, email: str, password: str):
        url_base: str = "https://mail-eu-south.testarea.zextras.com/"
        self._url_graphql: str = url_base + "zx/drive/graphql/v1/"
        self._url_files: str = url_base + "service/extension/drive/"

        self._email = email
        self._user_id = ""
        self._env_settings = QSettings()

        session = CookieSession(email, password)

        if not session.is_logged():
            raise ValueError("Email o password non valide")

        self._cookie = session.get_auth_token()

        _headers = {
            "Content-Type": "application/json",
            "cookie": self._cookie
        }

        _transport = RequestsHTTPTransport(
            url=self._url_graphql,
            headers=_headers,
            use_json=True
        )

        self.client = Client(transport=_transport, fetch_schema_from_transport=True)
        self._logger = logging.getLogger("server")

    def get_info_from_email(self) -> dict[str, str]:
        """Ritorna l'id e il nome dell'account"""
        query, params = Query.get_info_from_email(self._email)
        response = self.client.execute(gql(query), variable_values=params)
        return response["getUserByEmail"]

    def get_user_id(self) -> str:
        """Metodo che recupera l'id se non scaricato in precedenza"""
        if self._user_id == "":
            self._user_id = self.get_info_from_email()["id"]
        return self._user_id

    def get_all_files(self, node_id: str = "LOCAL_ROOT") -> list:
        """Restituisce il nome dei file con l'ultima modifica"""
        query, params = Query.get_all_files(node_id)
        response = self.client.execute(gql(query), variable_values=params)
        result: list = []
        for files in response["getNode"]["children"]:
            # Tenere questa linea fino a quando non caricheremo
            # anche le cartelle
            if files["type"] == "File":
                # Bisogna dividere la data per 1000,
                # Zextras la restituisce in millisecondi
                result.append({
                    "id": files["id"],
                    "name": files["name"],
                    "updated_at": files["updated_at"] / 1000,
                    "created_at": files["created_at"] / 1000,
                    "size": files["size"]
                })
        self._logger.info(f"File presenti nel server: {len(result)} files")
        return result

    def upload_to_server(self, file_path: str) -> None:
        """Richiede il file_path"""
        headers = {
            "cookie": self._cookie
        }

        file_name = os.path.basename(file_path)
        updated_at = math.trunc(os.stat(file_path).st_mtime)
        created_at = math.trunc(os.stat(file_path).st_ctime)
        # TODO:
        # - Da capire come gestire le cartelle
        multipart_form = {
            "command": "upload",
            "name": file_name,
            "content": open(file_path, "rb"),
            "parent": self.get_user_id() + "/LOCAL_ROOT",
            "updated-at": updated_at,
            "created-at": created_at
        }

        response = requests.post(self._url_files, headers=headers, files=multipart_form)

        if response.status_code == requests.codes.ok:
            self._logger.info(f"Upload del file {file_name}, completato con successo")
        else:
            self._logger.info(f"Upload del file {file_name}, fallito")
        return response.status_code == requests.codes.ok

    def download_from_server(self,
                             file_path: str,
                             file_name: str,
                             file_id: str,
                             created_at: int,
                             updated_at: int) -> None:
        """ Scarica il file dal server e lo salva nel path,
            filename con l'estensione e path
        """
        headers = {
            "cookie": self._cookie
        }
        url = f"{self._url_files}{self.get_user_id()}/{file_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == requests.codes.ok:
            self._logger.info(f"Download del file {file_name}, completato con successo")
            path = os.path.join(file_path, file_name)
            with open(path, "wb") as fh:
                fh.write(response.content)
            # Cambiare la data di creazione sembra non funzionare
            os.utime(path, (created_at, updated_at))
        else:
            self._logger.info(f"Download del file {file_name}, fallito")
