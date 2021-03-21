import os
import logging
import requests
import math
from .query_model import Query
from .cookie_session import CookieSession
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

url_base = "https://mail-eu-south.testarea.zextras.com/"
url_graphql = url_base + "zx/drive/graphql/v1/"
url_files = url_base + "service/extension/drive/"

email = ""  # settings.get_username()
password = ""  # settings.get_password()
user_id = ""
cookie = None
client = None
logger = logging.getLogger("server")
session = None


def login(_email: str, _pwd: str):
    global cookie
    global client
    global session
    session = CookieSession(_email, _pwd)

    if not session.is_logged():
        raise ValueError("Email o password non valide")
    cookie = session.get_auth_token()

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


def is_logged():
    return session if session is not None else False


def set_username_and_pwd(_email: str, _pwd: str) -> None:
    global email
    global password
    email = _email
    password = _pwd


def get_info_from_email() -> dict[str, str]:
    """Ritorna l'id e il nome dell'account"""
    query, params = Query.get_info_from_email(email)
    response = client.execute(gql(query), variable_values=params)
    return response["getUserByEmail"]


def get_user_id() -> str:
    """Metodo che recupera l'id se non scaricato in precedenza"""
    global user_id
    if user_id == "":
        user_id = get_info_from_email()["id"]
    return user_id


def get_all_files(node_id: str = "LOCAL_ROOT") -> list:
    """Restituisce il nome dei file con l'ultima modifica"""
    query, params = Query.get_all_files(node_id)
    response = client.execute(gql(query), variable_values=params)
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
    logger.info(f"File presenti nel server: {len(result)} files")
    return result


def upload_to_server(file_path: str) -> None:
    """Richiede il file_path"""
    headers = {
        "cookie": cookie
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
        "parent": get_user_id() + "/LOCAL_ROOT",
        "updated-at": updated_at,
        "created-at": created_at
    }

    response = requests.post(url_files, headers=headers, files=multipart_form)

    if response.status_code == requests.codes.ok:
        logger.info(f"Upload del file {file_name}, completato con successo")
    else:
        logger.info(f"Upload del file {file_name}, fallito")
    return response.status_code == requests.codes.ok


def download_from_server(
        file_path: str,
        file_name: str,
        file_id: str,
        created_at: int,
        updated_at: int) -> None:
    """ Scarica il file dal server e lo salva nel path,
        filename con l'estensione e path
    """
    headers = {
        "cookie": cookie
    }
    url = f"{url_files}{get_user_id()}/{file_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        logger.info(f"Download del file {file_name}, completato con successo")
        path = os.path.join(file_path, file_name)
        with open(path, "wb") as fh:
            fh.write(response.content)
        # Cambiare la data di creazione sembra non funzionare
        os.utime(path, (created_at, updated_at))
    else:
        logger.info(f"Download del file {file_name}, fallito")
