import os
import logging
import requests
from .query_model import Query
from src.model.network.tree_node import TreeNode
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from .api_exceptions import (LoginError, NetworkError, ServerError, NetworkErrs, ServerErrs)

from requests.utils import dict_from_cookiejar
from requests import Session

"""

Exceptions
----------
il modulo puo lanciare le seguenti eccezzioni:

LoginError: in caso di credenziali non valide

NetworkError: in caso di errori dovuti alla connessione (internet down, DNS failure, ecc) 

ServerError: in caso di risposte errate da parte del server o del protocollo http in generale

"""


url_base = "https://mail-eu-south.testarea.zextras.com/"
url_graphql = url_base + "zx/drive/graphql/v1/"
url_files = url_base + "service/extension/drive/"

email = ""
password = ""
user_id = ""
cookie: dict = None
client = None
logger = logging.getLogger("API")


def ExceptionsHandler(func):
    global logger

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NetworkErrs as e:
            logger.error(f"ExceptionsHandler found {str(e)}")
            logger.error("ExceptionsHandler: raise NetworkError")
            raise NetworkError(f"{func.__name__}: {str(e)}")
        except ServerErrs as e:
            logger.error(f"ExceptionsHandler found {str(e)}")
            logger.error("ExceptionsHandler: raise ServerError")
            raise ServerError()

    return inner


def check_status_code(response):
    global logger

    logger.debug(f"handle response code...{response.status_code}")

    # 401 è chiaramente un problema di login
    if response.status_code == 401:
        logger.error("401 Unauthorized: raise LoginError")
        raise LoginError()

    # alza un'ecezzione di tipo HTTPError solo in caso di codici di errore
    # l'eccezzione è intercettata dal gruppo ServerErrs
    response.raise_for_status()


def cookie2str(cookie: dict) -> str:
    if cookie:
        return "; ".join([f"{str(x)}={str(y)}" for x, y in cookie.items()])
    return ""


@ExceptionsHandler
def is_logged(_cookie: str = "") -> bool:
    global logger
    global cookie
    logger.debug("checking login status...")

    def OK():
        logger.debug("logged")
        return True
    
    def KO():
        logger.debug("not logged")
        return False

    c = _cookie if _cookie else cookie
    r = requests.get(url_base, headers={"cookie":c})
    KO() if "LoginScreen" in r.text else OK()


@ExceptionsHandler
def login(_email: str = "", _pwd: str = "") -> bool:
    global url_base
    global cookie
    global email
    global password
    global logger
    logger.debug("start login procedure...")

    def csrf(session) -> str:
        # estraggo il codice csrf dai cookie di sessione
        try:
            _cookies = dict_from_cookiejar(session.cookies)
            csrf = _cookies['ZM_LOGIN_CSRF']
            if csrf:
                logger.debug("CSRF code found")
                return csrf
        except Exception:
            logger.error("NO CSRF code found")
            logger.error("raise ServerError")
            raise ServerError("NO CSRF code found")

    if is_logged():
        return True

    session = Session()

    # questa chiamata setta i cookie di sessione che conterranno il codice csrf
    logger.debug("getting CSRF code from zextras")
    r = session.get(url_base)
    check_status_code(r)

    # dati estrapolati dalla chiamata post di login nel browser
    # il codice csrf è generato dinamicamente
    # da una chiamata get all'interfaccia web
    login = {
        "loginOp": "login",
        "login_csrf": csrf(session),
        "username": _email if _email else email,
        "password": _pwd if _pwd else password,
        "zrememberme": 1,
        "client": "preferred"
    }

    logger.debug("sending login POST request")
    r = session.post(url_base, data=login)
    check_status_code(r)

    new_cookie = cookie2str(dict_from_cookiejar(session.cookies))

    # se è andata bene i nuovi cookie di sessione
    # contengono il token di autenticazione
    if is_logged(new_cookie):
        # setto i nuovi parametri
        logger.debug("setting new cookie and credentials")
        email = _email
        password = _pwd
        cookie = new_cookie

        logger.debug(f"NEW COOKIE {cookie}")

        init_client()
        return True
    else:
        # se arrivo qui non mi sono loggato
        logger.error("raise LoginError")
        raise LoginError()


@ExceptionsHandler
def init_client():
    global client
    global logger
    logger.debug("setting client")

    _headers = {
        "Content-Type": "application/json",
        "cookie": cookie
    }

    _transport = RequestsHTTPTransport(
        url=url_graphql,
        headers=_headers,
        use_json=True
    )

    client = Client(transport=_transport, fetch_schema_from_transport=True)


@ExceptionsHandler
def logout() -> bool:
    global cookie
    global client
    global logger

    cookie = None
    client = None
    logger.debug("logout")
    return True


@ExceptionsHandler
def set_username_and_pwd(_email: str, _pwd: str) -> None:
    global email
    global password
    email = _email
    password = _pwd


@ExceptionsHandler
def get_info_from_email() -> dict[str, str]:
    """Ritorna l'id e il nome dell'account"""
    global email
    global logger
    logger.debug(f"getting info from email: {email}")

    query, params = Query.get_info_from_email(email)
    response = client.execute(gql(query), variable_values=params)

    try:
        info = response["getUserByEmail"]
        logger.debug(f"info: {info}")
        return info
    except Exception as e:
        logger.error(f"{str(e)}")
        logger.error("raise ServerError")
        raise ServerError(f"{str(e)}")


@ExceptionsHandler
def get_user_id() -> str:
    """Metodo che recupera l'id se non scaricato in precedenza"""
    global user_id
    if user_id == "":
        user_id = get_info_from_email()["id"]
    return user_id


@ExceptionsHandler
def get_content_from_node(node_id: str = "LOCAL_ROOT") -> str:
    query, params = Query.get_all_files(node_id)
    return client.execute(gql(query), variable_values=params)


@ExceptionsHandler
def create_folder(folder_name: str, parent_folder_id: str = "LOCAL_ROOT") -> str:
    """Ritorna l'id della cartella appena creata"""
    query, params = Query.create_folder(parent_folder_id, folder_name)
    response = client.execute(gql(query), variable_values=params)
    return response["createFolder"]["id"]


def download_node_from_server(node: TreeNode, path: str) -> None:
    """Il TreeNode viene scaricato e salvato nel path"""
    headers = {
        "cookie": cookie
    }
    payload = node._payload
    url = f"{url_files}{get_user_id()}/{payload.id}"
    response = requests.get(url, headers=headers)

    if response.ok:
        path = os.path.join(path, payload.name)
        with open(path, "wb") as fh:
            fh.write(response.content)
        # Cambiare la data di creazione sembra non funzionare
        os.utime(path, (payload.created_at, payload.updated_at))
        logger.info(f"Download del file {payload.name}, completato con successo")
    else:
        logger.info(f"Download del file {payload.name}, fallito")
        # alzo le eccezzioni del caso
        check_status_code(response)


def upload_node_to_server(node: TreeNode, parent_id: str = "LOCAL_ROOT"):
    """Carica un nodo, all'interno del parent passato"""
    headers = {
        "cookie": cookie
    }

    name = node.get_name()
    content = open(node._payload.path, "rb")
    updated_at = node.get_updated_at()
    created_at = node._payload.created_at

    multipart_form = {
        "command": "upload",
        "name": name,
        "content": content,
        "parent": get_user_id() + "/" + parent_id,
        "updated-at": updated_at,
        "created-at": created_at
    }

    response = requests.post(url_files, headers=headers, files=multipart_form)

    if response.ok:
        logger.info(f"Upload del file {name}, completato con successo")
    else:
        logger.info(f"Upload del file {name}, fallito")
        # alzo le eccezzioni del caso
        check_status_code(response)
