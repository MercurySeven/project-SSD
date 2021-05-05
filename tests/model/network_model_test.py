from unittest.mock import patch

from src.model.main_model import MainModel
from src.network.api_implementation import LoginError, NetworkError, ServerError
from tests import default_code


class NetworkModelTest(default_code.DefaultCode):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()
        self.main_model = MainModel()
        self.model_test = self.main_model.network_model

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()

    @patch('src.network.api_implementation.ApiImplementation.login', return_value=False)
    def test_login_value_exception(self, mocked_function):
        self.model_test.login("test", "test")
        mocked_function.assert_called_once()
        self.assertFalse(self.model_test.is_logged())

    @patch('src.network.api_implementation.ApiImplementation.login', return_value=False)
    def test_login_network_response_exception(self, mocked_function):
        exception_string = "Errore nella connessione con i server Zextras"
        mocked_function.side_effect = NetworkError(exception_string)
        # self.assertRaises(ValueError, self.model_test.login("test", "test"))
        self.model_test.login("test", "test")
        self.assertFalse(self.model_test.is_logged())
        mocked_function.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.login', return_value=False)
    def test_login_response_exception(self, mocked_function):
        exception_string = "Login error"
        mocked_function.side_effect = LoginError(exception_string)
        self.model_test.login("test", "test")
        self.assertFalse(self.model_test.is_logged())
        mocked_function.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.login', return_value=False)
    def test_login_server_response_exception(self, mocked_function):
        exception_string = "Server error"
        mocked_function.side_effect = ServerError(exception_string)
        self.model_test.login("test", "test")
        self.assertFalse(self.model_test.is_logged())
        mocked_function.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.login', return_value=True)
    @patch('src.network.api_implementation.ApiImplementation.is_logged', return_value=True)
    def test_login_success(self, mocked_is_logged_in, mocked_login):
        self.model_test.login("test", "test")
        mocked_login.assert_called_once()
        self.assertTrue(self.model_test.is_logged())
        mocked_is_logged_in.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.logout', return_value=True)
    def test_logout_success(self, mock_api_logout):
        self.assertEqual(self.model_test.logout(), True)
        mock_api_logout.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.logout', return_value=False)
    def test_logout_failure(self, mock_api_logout):
        self.assertEqual(self.model_test.logout(), False)
        mock_api_logout.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.get_content_from_node',
           return_value=default_code._get_tree_dict())
    @patch('src.network.api_implementation.ApiImplementation.download_node',
           return_value=True)
    def test_download_success(self, download_mock, get_content_mock):
        expected_result = {
            "node_name": default_code._get_test_node().get_name(),
            "result": True,
            "type": ""
        }
        result = self.model_test.download_node(default_code._get_test_node(), "test", 100)
        download_mock.assert_called_once()
        get_content_mock.assert_called_once()
        self.assertEqual(result, expected_result)

    @patch('src.network.api_implementation.ApiImplementation.get_content_from_node',
           return_value=default_code._get_tree_dict())
    @patch('src.network.api_implementation.ApiImplementation.download_node',
           return_value=False)
    def test_download_fail_for_quota(self, download_mock, get_content_mock):
        expected_result = {
            "node_name": default_code._get_test_node().get_name(),
            "result": False,
            "type": "space_error"
        }
        result = self.model_test.download_node(default_code._get_test_node(), "test", 0)
        get_content_mock.assert_called_once()
        self.assertEqual(download_mock.call_count, 0)
        self.assertEqual(result, expected_result)

    @patch('src.network.api_implementation.ApiImplementation.get_content_from_node',
           return_value=default_code._get_tree_dict())
    @patch('src.network.api_implementation.ApiImplementation.download_node',
           return_value=False)
    def test_download_fail_for_network_error(self, download_mock, get_content_mock):
        expected_result = {
            "node_name": default_code._get_test_node().get_name(),
            "result": False,
            "type": "network_error"
        }
        result = self.model_test.download_node(default_code._get_test_node(), "test", 100)
        download_mock.assert_called_once()
        get_content_mock.assert_called_once()
        self.assertEqual(result, expected_result)
