import unittest
from unittest.mock import patch

from src.network import api
from tests import default_code


class ApiTest(unittest.TestCase):
    class RequestObj:
        def __init__(self, _text: str = "test"):
            self.text = _text

        def set_text(self, _text):
            self.text = _text

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
