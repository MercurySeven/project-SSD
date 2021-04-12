import os
import logging
import requests

from .api import Api
from .query_model import Query
from src.model.algorithm.tree_node import TreeNode
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from .api_exceptions import (LoginError, NetworkError, ServerError, NetworkErrs, ServerErrs)

from requests.utils import dict_from_cookiejar
from requests import Session

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
        self.url_files = self.url_base + "service/extension/drive/"

        self.email = ""
        self.password = ""
        self.user_id = ""
        self.cookie: dict = None
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

    def cookie2str(self, cookie: dict) -> str:
        for key, value in cookie.items():
            if key == "ZM_AUTH_TOKEN":
                return "ZM_AUTH_TOKEN=" + value
        return ""

    @ExceptionsHandler
    def is_logged(self, _cookie: str = "") -> bool:
        self.logger.debug("checking login status...")

        def OK():
            self.logger.debug("logged")
            return True

        def KO():
            self.logger.debug("not logged")
            return False

        c = _cookie if _cookie else self.cookie
        r = requests.get(self.url_base, headers={"cookie": c})
        return KO() if "LoginScreen" in r.text else OK()

    @ExceptionsHandler
    def login(self, _email: str = "", _pwd: str = "") -> bool:
        self.logger.debug("start login procedure...")

        def csrf(session) -> str:
            # estraggo il codice csrf dai cookie di sessione
            try:
                _cookies = dict_from_cookiejar(session.cookies)
                csrf = _cookies['ZM_LOGIN_CSRF']
                if csrf:
                    self.logger.debug("CSRF code found")
                    return csrf
            except Exception:
                self.logger.error("NO CSRF code found")
                self.logger.error("raise ServerError")
                raise ServerError("NO CSRF code found")

        if self.is_logged():
            return True

        session = Session()

        # questa chiamata setta i cookie di sessione che conterranno il codice csrf
        self.logger.debug("getting CSRF code from zextras")
        r = session.get(self.url_base)
        self.check_status_code(r)

        # dati estrapolati dalla chiamata post di login nel browser
        # il codice csrf è generato dinamicamente
        # da una chiamata get all'interfaccia web
        login = {
            "loginOp": "login",
            "login_csrf": csrf(session),
            "username": _email if _email else self.email,
            "password": _pwd if _pwd else self.password,
            "zrememberme": 1,
            "client": "preferred"
        }

        self.logger.debug("sending login POST request")
        r = session.post(self.url_base, data=login)
        self.check_status_code(r)

        new_cookie = self.cookie2str(dict_from_cookiejar(session.cookies))

        # se è andata bene i nuovi cookie di sessione
        # contengono il token di autenticazione
        if self.is_logged(new_cookie):
            # setto i nuovi parametri
            self.logger.debug("setting new cookie and credentials")
            self.email = _email
            self.password = _pwd
            self.cookie = new_cookie
            print(self.cookie)

            self.init_client()
            return True
        else:
            # se arrivo qui non mi sono loggato
            self.logger.error("raise LoginError")
            raise LoginError()

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

        self.cookie = None
        self.client = None
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
        if self.user_id == "":
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
        query, params = Query.delete_node(node_id)
        self.client.execute(gql(query), variable_values=params)

    @ExceptionsHandler
    def download_node(self, node: TreeNode, path: str) -> None:
        """Il TreeNode viene scaricato e salvato nel path"""
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
        else:
            self.logger.info(f"Download del file {payload.name}, fallito")
            # alzo le eccezioni del caso
            self.check_status_code(response)

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
