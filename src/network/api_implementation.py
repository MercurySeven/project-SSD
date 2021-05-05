import logging
import os

import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from src.model.algorithm.tree_node import TreeNode
from .api import Api
from .api_exceptions import (LoginError, NetworkError, ServerError, NetworkErrs, ServerErrs)
from .query_model import Query

"""

Exceptions
----------
il modulo puo lanciare le seguenti eccezioni:

LoginError: in caso di credenziali non valide

NetworkError: in caso di errori dovuti alla connessione (internet down, DNS failure, ecc)

ServerError: in caso di risposte errate da parte del server o del protocollo http in generale

"""


def ExceptionsHandler(func):
    logger = logging.getLogger("API.ExceptionsHandler")

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NetworkErrs as e:
            logger.error(f"found {str(e)}")
            logger.error("raise NetworkError")
            raise NetworkError(f"{func.__name__}: {str(e)}")
        except ServerErrs as e:
            logger.error(f"found {str(e)}")
            logger.error("raise ServerError")
            raise ServerError()

    return inner


class ApiImplementation(Api):

    def __init__(self):
        self.url_base = "https://mail-eu-south.testarea.zextras.com/"
        self.url_graphql = self.url_base + "zx/drive/graphql/v1/"
        self.url_login = self.url_base + "zx/team/login"
        self.url_files = self.url_base + "service/extension/drive/"

        self.email = ""
        self.password = ""
        self.cookie = ""
        self.user_id = None
        self.client = None
        self.logger = logging.getLogger("API")

    def check_status_code(self, response):
        self.logger.debug(f"handle response code...{response.status_code}")

        # 401 è chiaramente un problema di login
        if response.status_code == 401:
            self.logger.error("401 Unauthorized: raise LoginError")
            raise LoginError()

        # alza un'ecezzione di tipo HTTPError solo in caso di codici di errore
        # l'eccezione è intercettata dal gruppo ServerErrs
        response.raise_for_status()

    @ExceptionsHandler
    def is_logged(self) -> bool:
        self.logger.debug("checking login status...")

        r = requests.get(self.url_base, headers={"cookie": self.cookie})

        if "LoginScreen" in r.text:
            self.logger.debug("not logged")
            return False
        else:
            self.logger.debug("logged")
            return True

    @ExceptionsHandler
    def login(self, _email: str = "", _pwd: str = ""):
        self.logger.debug("start login procedure...")

        payload = {
            "auth_method": "password",
            "email": _email if _email else self.email,
            "password": _pwd if _pwd else self.password,
            "min_api_version": 1,
            "max_api_version": 10
        }

        self.logger.debug("sending login POST request")
        r = requests.post(self.url_login, json=payload)

        # check for login errors
        self.check_status_code(r)

        self.logger.debug("setting new cookie and credentials")
        self.email = _email
        self.password = _pwd
        self.user_id = r.json()['user_info']['id']
        self.cookie = r.json()['auth_token']['cookie']

        # Non cancellare questa linea, è utile per recuperare facilmente il cookie :)
        print(self.cookie)

        self.init_client()

    @ExceptionsHandler
    def init_client(self):
        self.logger.debug("setting client")

        _headers = {
            "Content-Type": "application/json",
            "cookie": self.cookie
        }

        _transport = RequestsHTTPTransport(
            url=self.url_graphql,
            headers=_headers,
            use_json=True
        )

        self.client = Client(transport=_transport, fetch_schema_from_transport=True)

    @ExceptionsHandler
    def logout(self) -> bool:
        self.cookie = ""
        self.client = None
        self.user_id = None
        self.logger.debug("logout")
        return True

    @ExceptionsHandler
    def get_info_from_email(self) -> dict[str, str]:
        """Ritorna l'id e il nome dell'account"""
        self.logger.debug(f"getting info from email: {self.email}")

        query, params = Query.get_info_from_email(self.email)
        response = self.client.execute(gql(query), variable_values=params)

        try:
            info = response["getUserByEmail"]
            self.logger.debug(f"info: {info}")
            return info
        except Exception as e:
            self.logger.error(f"{str(e)}")
            self.logger.error("raise ServerError")
            raise ServerError(f"{str(e)}")

    @ExceptionsHandler
    def get_user_id(self) -> str:
        """Metodo che recupera l'id se non scaricato in precedenza"""
        if not self.user_id:
            self.user_id = self.get_info_from_email()["id"]
        return self.user_id

    @ExceptionsHandler
    def get_content_from_node(self, node_id: str = "LOCAL_ROOT") -> str:
        query, params = Query.get_all_files(node_id)
        return self.client.execute(gql(query), variable_values=params)

    @ExceptionsHandler
    def create_folder(self, folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
        """Ritorna l'id della cartella appena creata"""
        query, params = Query.create_folder(parent_folder_id, folder_name)
        response = self.client.execute(gql(query), variable_values=params)
        return response["createFolder"]["id"]

    @ExceptionsHandler
    def delete_node(self, node_id: str) -> None:
        """Rimuove il nodo dato l'id"""
        if node_id != "LOCAL_ROOT":
            query, params = Query.delete_node(node_id)
            self.client.execute(gql(query), variable_values=params)
        else:
            print("NON PUOI CANCELLARE LOCAL_ROOT")

    @ExceptionsHandler
    def download_node(self, node: TreeNode, path: str) -> bool:
        """Il TreeNode viene scaricato e salvato nel path, ritorna un bool a seconda dell'esito"""
        headers = {
            "cookie": self.cookie
        }
        payload = node.get_payload()
        url = f"{self.url_files}{self.get_user_id()}/{payload.id}"
        response = requests.get(url, headers=headers)

        if response.ok:
            path = os.path.join(path, payload.name)
            with open(path, "wb") as fh:
                fh.write(response.content)
            # Cambiare la data di creazione sembra non funzionare
            os.utime(path, (payload.created_at, payload.updated_at))
            self.logger.info(f"Download del file {payload.name}, completato con successo")
            return True
        else:
            self.logger.info(f"Download del file {payload.name}, fallito")
            # alzo le eccezioni del caso
            self.check_status_code(response)
            return False

    @ExceptionsHandler
    def upload_node(self, node: TreeNode, parent_id: str = "LOCAL_ROOT"):
        """Carica un nodo, all'interno del parent passato"""
        headers = {
            "cookie": self.cookie
        }

        name = node.get_name()
        content = open(node.get_payload().path, "rb")
        updated_at = node.get_updated_at()
        created_at = node.get_payload().created_at

        multipart_form = {
            "command": "upload",
            "name": name,
            "content": content,
            "parent": self.get_user_id() + "/" + parent_id,
            "updated-at": updated_at,
            "created-at": created_at
        }

        response = requests.post(self.url_files, headers=headers, files=multipart_form)

        if response.ok:
            self.logger.info(f"Upload del file {name}, completato con successo")
        else:
            self.logger.info(f"Upload del file {name}, fallito")
            # alzo le eccezioni del caso
            self.check_status_code(response)
