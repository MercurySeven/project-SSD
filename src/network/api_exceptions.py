from requests.exceptions import RequestException
from gql.transport.exceptions import TransportError, TransportQueryError


class APIException(Exception):
    """eccezzione generica del modulo API."""

    def __init__(self, message: str = ""):
        super(APIException, self).__init__(message)


class LoginError(APIException):
    """eccezzione lanciata in caso di credenziali errate"""

    def __init__(self, message: str = ""):
        super(LoginError, self).__init__(message)


class NetworkError(APIException):
    """eccezzione anciata in caso di problermi dovuti alla rete:
    connessione assente o server irraggiungibile

    raggruppati in NetworkErrs"""

    def __init__(self, message: str = ""):
        super(NetworkError, self).__init__(message)


class ServerError(APIException):
    """eccezzione lanciata in caso di errori dovuti alle risposte del server
    raggruppati in ServerErrs"""

    def __init__(self, message: str = ""):
        super(ConnectionError, self).__init__(message)


# TODO migliorare la granularità delle eccezzioni, cosi è troppo generale

NetworkErrs = (
    RequestException
)

ServerErrs = (
    TransportError,
    TransportQueryError
)