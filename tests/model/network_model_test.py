import os
import pathlib
import unittest
from unittest.mock import patch

from src import settings
from src.model.network_model import NetworkModel
from src.network.cookie_session import BadResponse


class NetworkModelTest(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.path = os.path.join(str(pathlib.Path().absolute()), "tests")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        settings.file_name = os.path.join(self.path, "config.ini")
        settings.check_file()
        self.model_test = NetworkModel()

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(settings.file_name)

    @patch('src.network.cookie_session.CookieSession._login', return_value=False)
    def test_login_value_exception(self, mocked_function):
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())

    @patch('src.network.cookie_session.CookieSession._login', return_value=False)
    def test_login_connection_exception(self, mocked_function):
        exception_string = "Errore nella connessione con i server Zextras"
        mocked_function.side_effect = ConnectionError(exception_string)
        # self.assertRaises(ValueError, self.model_test.login("test", "test"))
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())
        self.assertEqual(exception_string, self.model_test.get_message())

    @patch('src.network.cookie_session.CookieSession._login', return_value=False)
    def test_login_bad_response_exception(self, mocked_function):
        exception_string = "Bad response: test test test"
        mocked_function.side_effect = BadResponse("test", "test", "test")
        # self.assertRaises(ValueError, self.model_test.login("test", "test"))
        self.model_test.login("test", "test")
        self.assertEqual(False, self.model_test.is_logged())
        self.assertEqual(exception_string, self.model_test.get_message())

    @patch('src.network.cookie_session.CookieSession._login', return_value=True)
    def test_login_success(self, mocked_fun):
        self.model_test.login("test", "test")
        mocked_fun.assert_called_once()
        self.assertEqual(True, self.model_test.is_logged())
