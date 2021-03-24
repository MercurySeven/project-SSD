import os
import logging
import requests
from .query_model import Query
from .cookie_session import CookieSession
from src.model.network.tree_node import TreeNode
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from .api_exceptions import (LoginError, NetworkError, ServerError, NetworkErrs, ServerErrs)

from requests.utils import dict_from_cookiejar
from requests import Session


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

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NetworkErrs as e:
            raise NetworkError(f"{func.__name__}: {str(e)}")
        except ServerErrs as e:
            raise ServerError(f"{func.__name__}: {str(e)}")
    return inner


def cookie_str() -> str:
    global cookie
    if cookie:
        return "; ".join([f"{str(x)}={str(y)}" for x, y in cookie.items()])
    return ""


@ExceptionsHandler
def login(_email: str, _pwd: str):
    global cookie
    global client
    global session

    



    session = Session()

    if not session.is_logged():
        raise LoginError("Email o password non valide")
    cookie = session.get_auth_token()


@ExceptionsHandler
def init_client():

    global client

    _headers = {
        "Content-Type": "application/json",
        "cookie": cookie_str()
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
    global session
    cookie = None
    client = None
    session = None
    return True

@ExceptionsHandler
def is_logged():

    if client:
        try:
            get





    return session.is_logged() if session is not None else False


@ExceptionsHandler
def set_username_and_pwd(_email: str, _pwd: str) -> None:
    global email
    global password
    email = _email
    password = _pwd


@ExceptionsHandler
def get_info_from_email() -> dict[str, str]:
    """Ritorna l'id e il nome dell'account"""
    query, params = Query.get_info_from_email(email)
    response = client.execute(gql(query), variable_values=params)
    return response["getUserByEmail"]


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

    if response.status_code == requests.codes.ok:
        path = os.path.join(path, payload.name)
        with open(path, "wb") as fh:
            fh.write(response.content)
        # Cambiare la data di creazione sembra non funzionare
        os.utime(path, (payload.created_at, payload.updated_at))
        logger.info(f"Download del file {payload.name}, completato con successo")
    else:
        logger.info(f"Download del file {payload.name}, fallito")


def upload_node_to_server(node: TreeNode, parent_id: str = "LOCAL_ROOT") -> None:
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

    if response.status_code == requests.codes.ok:
        logger.info(f"Upload del file {name}, completato con successo")
    else:
        logger.info(f"Upload del file {name}, fallito")
    return response.status_code == requests.codes.ok
