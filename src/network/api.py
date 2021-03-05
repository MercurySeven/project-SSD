from requests.utils import dict_from_cookiejar
from requests import Session
import json


# custum error
class BadResponse(Exception):
    def __init__(self, protocol, code, url):
        super().__init__(f"Bad response: {protocol} {code} {url}")


class API:

    def __init__(self, username: str = "", password: str = ""):

        self.username = username
        self.password = password
        self.query_endpoint = "https://mail-eu-south.testarea.zextras.com/zx/drive/graphql/v1"
        self.up_down_endpoint = "https://mail-eu-south.testarea.zextras.com/service/extension/drive/"
        self.web_ui = "https://mail-eu-south.testarea.zextras.com/"
        self.session = Session()

        if self.username and self.password:
            self.login()

    def upload(self):
        # TODO
        pass

    def download(self):
        #  TODO
        pass

    def reset_session(self):
        self.session = Session()

    def auth(self, username: str, password: str):
        self.username = username
        self.password = password
        self.login()

    def is_logged(self):
        cookies = dict_from_cookiejar(self.session.cookies)
        return True if "ZM_AUTH_TOKEN" in cookies.keys() else False

    def csrf(self):
        # questa chiamata setta i cookie di sessione che conterranno il codice
        r = self.session.get(self.web_ui)
        if not r.ok:
            raise BadResponse("GET", r.status_code, self.web_ui)

        # estraggo il codice dai cookie ottenuti
        try:
            cookies = dict_from_cookiejar(self.session.cookies)
            return cookies['ZM_LOGIN_CSRF']
        except Exception:
            raise Exception("no CSRF code found")

    def set_custom_headers(self):
        headers = {
            "Content-type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",  # optional
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"  # optional
        }
        self.session.headers.update(headers)

    def login(self):
        if self.is_logged():
            return True

        if not (self.username and self.password):
            raise Exception("no username and password found")

        # dati estrapolati dalla chiamata post di login nel browser
        # il codice csrf è generato dinamicamente
        # da una chiamata get all'interfaccia web
        login = {
            "loginOp": "login",
            "login_csrf": self.csrf(),
            "username": self.username,
            "password": self.password,
            "client": "preferred"
        }

        r = self.session.post(self.web_ui, data=login)
        if not r.ok:
            raise BadResponse("POST", r.status_code, self.web_ui)

        # se è andata bene i nuovi cookie di sessione contengono il token di autenticazione
        if self.is_logged():
            # setto i nuovi headers di sessione cosi non servirà impostarli ad ogni chiamata
            self.set_custom_headers()
            return True
        return False

    def call(self, query: str) -> dict:

        params = {"query": query}

        r = self.session.post(self.query_endpoint, json=params)
        if not r.ok: 
            raise BadResponse("POST", r.status_code, self.query_endpoint)

        return json.loads(r.text)

    def get_user_info(self, mail: str) -> dict:

        query = """query {
            getUserByEmail(email: \""""+mail+"""\") {
                id
                email
                full_name
            }
        }"""

        return self.call(query)

    def get_node(self, id: str, version: int = None) -> dict:

        def foo(bar):
            print(f"fu{bar}")

        if version is None:
            query = """
            query {
                getNode(id: \""""+id+"""\") {
                    id
                    created_at
                    name
                    type
                    ...cartella
                    ...file
                }
            }

            fragment cartella on Folder {
                children(limit:5) {
                    ...file
                }
            }

            fragment file on File {
                id
                name
                created_at
                type
                size
                version
                starred
            }"""
        else:
            # TODO
            foo("ck")
            return {}

        return self.call(query)


if __name__ == "__main__":
    api = API("mer1", "Tullio2020.")
    print(api.is_logged())
    print(api.get_user_info("mer1@testarea.zextras.com"))
    print(api.get_node("LOCAL_ROOT"))
