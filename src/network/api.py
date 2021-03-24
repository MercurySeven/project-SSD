import os
import logging
import requests
from .query_model import Query
from .cookie_session import CookieSession
from src.algorithm.tree_node import TreeNode
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
        self._logger.info("COOKIE DI AUTH: " + self._cookie)

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

    def get_content_from_node(self, node_id: str = "LOCAL_ROOT") -> str:
        query, params = Query.get_all_files(node_id)
        return self.client.execute(gql(query), variable_values=params)

    def create_folder(self, folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
        """Ritorna l'id della cartella appena creata"""
        query, params = Query.create_folder(parent_folder_id, folder_name)
        response = self.client.execute(gql(query), variable_values=params)
        return response["createFolder"]["id"]

    def download_node_from_server(self,
                                  node: TreeNode,
                                  path: str) -> None:
        """Il TreeNode viene scaricato e salvato nel path"""
        headers = {
            "cookie": self._cookie
        }
        payload = node._payload
        url = f"{self._url_files}{self.get_user_id()}/{payload.id}"
        response = requests.get(url, headers=headers)

        if response.status_code == requests.codes.ok:
            path = os.path.join(path, payload.name)
            with open(path, "wb") as fh:
                fh.write(response.content)
            # Cambiare la data di creazione sembra non funzionare
            os.utime(path, (payload.created_at, payload.updated_at))
            self._logger.info(f"Download del file {payload.name}, completato con successo")
        else:
            self._logger.info(f"Download del file {payload.name}, fallito")

    def upload_node_to_server(self, node: TreeNode, parent_id: str = "LOCAL_ROOT") -> None:
        """Carica un nodo, all'interno del parent passato"""
        headers = {
            "cookie": self._cookie
        }

        name = node.get_name()
        content = open(node._payload.path, "rb")
        updated_at = node.get_updated_at()
        created_at = node._payload.created_at

        multipart_form = {
            "command": "upload",
            "name": name,
            "content": content,
            "parent": self.get_user_id() + "/" + parent_id,
            "updated-at": updated_at,
            "created-at": created_at
        }

        response = requests.post(self._url_files, headers=headers, files=multipart_form)

        if response.status_code == requests.codes.ok:
            self._logger.info(f"Upload del file {name}, completato con successo")
        else:
            self._logger.info(f"Upload del file {name}, fallito")
        return response.status_code == requests.codes.ok
