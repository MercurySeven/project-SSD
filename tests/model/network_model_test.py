import unittest
from unittest.mock import patch
from src.model.network_model import NetworkModel
from src.network.api import LoginError, NetworkError, ServerError
from tests import default_code


class NetworkModelTest(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.model_test = NetworkModel()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        default_code.tearDown(self.env_settings, self.restore_path)

    @patch('src.network.api.login', return_value=False)
    def test_login_value_exception(self, mocked_function):
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())

    @patch('src.network.api.login', return_value=False)
    def test_login_network_response_exception(self, mocked_function):
        exception_string = "Errore nella connessione con i server Zextras"
        mocked_function.side_effect = NetworkError(exception_string)
        # self.assertRaises(ValueError, self.model_test.login("test", "test"))
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())
        self.assertEqual(exception_string, self.model_test.get_message())

    @patch('src.network.api.login', return_value=False)
    def test_login_response_exception(self, mocked_function):
        exception_string = "Login error"
        mocked_function.side_effect = LoginError(exception_string)
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())
        self.assertEqual(exception_string, self.model_test.get_message())

    @patch('src.network.api.login', return_value=False)
    def test_login_server_response_exception(self, mocked_function):
        exception_string = "Server error"
        mocked_function.side_effect = ServerError(exception_string)
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())
        self.assertEqual(exception_string, self.model_test.get_message())

    @patch('src.network.api.login', return_value=True)
    @patch('src.network.api.is_logged', return_value=True)
    def test_login_success(self, mocked_is_logged_in, mocked_login):
        self.model_test.login("test", "test")
        mocked_login.assert_called_once()
        self.assertEqual(True, self.model_test.is_logged())
