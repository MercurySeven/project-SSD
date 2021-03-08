from requests.utils import dict_from_cookiejar
from requests import Session


class BadResponse(Exception):
    def __init__(self, protocol, code, url):
        super().__init__(f"Bad response: {protocol} {code} {url}")


class CookieSession:

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._web_ui = "https://mail-eu-south.testarea.zextras.com/"
        self._session = Session()
        self.__login()

    def is_logged(self) -> bool:
        cookies = dict_from_cookiejar(self._session.cookies)
        return True if "ZM_AUTH_TOKEN" in cookies.keys() else False

    def __csrf(self) -> str:
        # questa chiamata setta i cookie di sessione che conterranno il codice
        r = self._session.get(self._web_ui)
        if not r.ok:
            raise BadResponse("GET", r.status_code, self._web_ui)

        # estraggo il codice dai cookie ottenuti
        try:
            cookies = dict_from_cookiejar(self._session.cookies)
            return cookies['ZM_LOGIN_CSRF']
        except Exception:
            raise Exception("no CSRF code found")

    def __set_custom_headers(self) -> None:
        headers = {
            "Content-type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
            "User-Agent": "SSD Zextras Drive Desktop"
        }
        self._session.headers.update(headers)

    def __login(self) -> bool:
        if self.is_logged():
            return True

        if not (self._username and self._password):
            raise Exception("no username and password found")

        # dati estrapolati dalla chiamata post di login nel browser
        # il codice csrf è generato dinamicamente
        # da una chiamata get all'interfaccia web
        login = {
            "loginOp": "login",
            "login_csrf": self.__csrf(),
            "username": self._username,
            "password": self._password,
            "client": "preferred"
        }

        r = self._session.post(self._web_ui, data=login)
        if not r.ok:
            raise BadResponse("POST", r.status_code, self._web_ui)

        # se è andata bene i nuovi cookie di sessione
        # contengono il token di autenticazione
        if self.is_logged():
            # setto i nuovi headers di sessione cosi
            # non servirà impostarli ad ogni chiamata
            self.__set_custom_headers()
            return True
        return False

    def get_cookie_str(self) -> str:
        result: str = ""
        for cookie in self._session.cookies:
            result += f"{cookie.name}={cookie.value}; "
        return result
