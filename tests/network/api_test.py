import unittest
from unittest.mock import patch

import gql
import requests.exceptions

from src.network import api
from src.network.api import ExceptionsHandler
from src.network.api_exceptions import NetworkError, ServerError
from tests import default_code


class ApiTest(unittest.TestCase):
    class RequestObj:
        def __init__(self, _text: str = "test"):
            self.text = _text

        def set_text(self, _text):
            self.text = _text

        @ExceptionsHandler
        def function_network_exception(self):
            raise requests.exceptions.ConnectionError("test")

        @ExceptionsHandler
        def function_server_exception(self):
            raise requests.exceptions.HTTPError("test")

    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        default_code.tearDown(self.env_settings, self.restore_path)

    @patch('src.network.api.is_logged', return_value=True)
    def test_login_already_logged_in(self, mocked_function):
        result = api.login("test", "test")
        mocked_function.assert_called_once()
        self.assertEqual(result, True)

    @patch('requests.get', return_value=RequestObj("LoginScreen"))
    def test_is_logged_false(self, mocked_function):
        logged = api.is_logged("test")
        mocked_function.assert_called_once()
        self.assertEqual(logged, False)

    @patch('requests.get', return_value=RequestObj())
    def test_is_logged_true(self, mocked_function):
        logged = api.is_logged("test")
        mocked_function.assert_called_once()
        self.assertEqual(logged, True)

    def test_exception_handler_network_error(self):
        test_obj = ApiTest.RequestObj()
        try:
            test_obj.function_network_exception()
        except Exception as e:
            fun_name = "function_network_exception"
            exc_message = "test"

            self.assertEqual(str(e), str(NetworkError(f"{fun_name}: {exc_message}")))

    def test_exception_handler_server_error(self):
        test_obj = ApiTest.RequestObj()
        try:
            test_obj.function_server_exception()
        except Exception as e:
            self.assertEqual(str(e), str(ServerError()))

    def test_logout(self):
        self.assertEqual(api.logout(), True)
        self.assertEqual(api.cookie, None)
        self.assertEqual(api.client, None)

    @patch('gql.client.Client.__init__', return_value=None)
    def test_init_client(self, mocked_function):
        api.client = True
        self.assertEqual(api.client, True)
        api.init_client()
        mocked_function.assert_called_once()
        client = gql.client.Client()
        self.assertEqual(vars(api.client), vars(client))
