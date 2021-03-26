from requests.exceptions import (HTTPError, ConnectionError,
                                 Timeout, URLRequired, TooManyRedirects,
                                 MissingSchema, InvalidSchema, InvalidURL,
                                 InvalidHeader, ChunkedEncodingError, ContentDecodingError,
                                 StreamConsumedError, RetryError, UnrewindableBodyError)

from gql.transport.exceptions import TransportError, TransportQueryError


class APIException(Exception):
    """eccezzione generica del modulo API."""

    def __init__(self, message: str = ""):
        super(APIException, self).__init__(message)


class LoginError(APIException):
    """eccezzione lanciata in caso di credenziali errate"""

    def __init__(self, message: str = "Credenziali non valide"):
        super(LoginError, self).__init__(message)


class NetworkError(APIException):
    """
    eccezzione anciata in caso di problermi dovuti alla rete:
    connessione assente o server irraggiungibile

    le possibili eccezzioni sono raggruppate in: NetworkErrs"""

    def __init__(self, message: str = ""):
        super(NetworkError, self).__init__(message)


class ServerError(APIException):
    """
    eccezzione lanciata in caso di errori dovuti alle risposte del server
    oppure se questo risulta irraggiungibile

    le possibili eccezzioni sono raggruppate in: ServerErrs"""

    def __init__(self, message: str = ""):
        super(ConnectionError, self).__init__(message)


NetworkErrs = (
    ConnectionError,
    Timeout
)

ServerErrs = (
    HTTPError,
    URLRequired,
    TooManyRedirects,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    InvalidHeader,
    ChunkedEncodingError,
    ContentDecodingError,
    StreamConsumedError,
    RetryError,
    UnrewindableBodyError,
    TransportError,
    TransportQueryError
)
