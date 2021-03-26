from requests.exceptions import (HTTPError, ConnectionError,
                                 Timeout, URLRequired, TooManyRedirects,
                                 MissingSchema, InvalidSchema, InvalidURL,
                                 InvalidHeader, ChunkedEncodingError, ContentDecodingError,
                                 StreamConsumedError, RetryError, UnrewindableBodyError)

from gql.transport.exceptions import TransportError, TransportQueryError


class APIException(Exception):
    """eccezione generica del modulo API."""

    def __init__(self, message: str = ""):
        super(APIException, self).__init__(message)


class LoginError(APIException):
    """eccezione lanciata in caso di credenziali errate"""

    def __init__(self, message: str = "Credenziali non valide"):
        super(LoginError, self).__init__(message)


class NetworkError(APIException):
    """
    eccezione anciata in caso di problermi dovuti alla rete:
    connessione assente o server irraggiungibile

    le possibili eccezioni sono raggruppate in: NetworkErrs"""

    def __init__(self, message: str = ""):
        super(NetworkError, self).__init__(message)


class ServerError(APIException):
    """
    eccezione lanciata in caso di errori dovuti alle risposte del server
    oppure se questo risulta irraggiungibile

    le possibili eccezioni sono raggruppate in: ServerErrs"""

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
