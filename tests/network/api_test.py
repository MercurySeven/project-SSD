import os
import pathlib
import unittest
from unittest.mock import patch

import gql
import requests.exceptions

from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import Status
from src.network import api
from src.network.api import ExceptionsHandler
from src.network.api_exceptions import NetworkError, ServerError, APIException, LoginError
from tests import default_code


class ApiTest(unittest.TestCase):
    class RequestObj:
        def __init__(self, _text: str = "test", _status: Status = Status.Ok):
            self.text = _text
            self.status_code = _status
            self.ok = _status if _status == Status.Ok else None
            self.content = b"test"

        def set_text(self, _text):
            self.text = _text

        @ExceptionsHandler
        def function_network_exception(self):
            raise requests.exceptions.ConnectionError("test")

        @ExceptionsHandler
        def function_server_exception(self):
            raise requests.exceptions.HTTPError("test")

        def raise_for_status(self):
            if self.status_code == Status.Error:
                raise APIException()

    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]

        self.file_name = "test.txt"

        self.original_path = self.env_settings.value("sync_path")

        self.path = os.path.join(self.original_path, "tree")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        default_code.tearDown(self.env_settings, self.restore_path)
        to_remove = os.path.join(self.path, self.file_name)
        if os.path.exists(to_remove):
            try:
                os.remove(to_remove)
            except PermissionError as e:
                print(e)
        os.rmdir(self.path)

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

    @patch('src.network.query_model.Query.get_info_from_email',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value=None)
    def test_get_info_from_email_exception_response_null(self, mocked_info, mocked_response):
        api.client = gql.client.Client()
        try:
            api.get_info_from_email()
        except Exception as e:
            self.assertEqual(str(e), str(ServerError("\'NoneType\' object is not subscriptable")))
        finally:
            mocked_info.assert_called_once()
            mocked_response.assert_called_once()

    @patch('src.network.query_model.Query.get_info_from_email',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"getUserByEmail": "test"})
    def test_get_info_from_email_success(self, mocked_info, mocked_response):
        self.assertEqual(api.get_info_from_email(), "test")
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    @patch('src.network.api.get_info_from_email', return_value={"id": "test"})
    def test_get_user_id(self, mocked_fun):
        api.user_id = ""
        self.assertEqual(api.get_user_id(), "test")
        mocked_fun.assert_called_once()

    @patch('src.network.query_model.Query.get_all_files',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"getUserByEmail": "test"})
    def test_get_content_from_node(self, mocked_info, mocked_response):
        api.client = gql.client.Client()
        self.assertEqual(api.get_content_from_node(), {"getUserByEmail": "test"})
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    @patch('src.network.query_model.Query.create_folder',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"createFolder": {"id": "test"}})
    def test_create_folder(self, mocked_info, mocked_response):
        api.client = gql.client.Client()
        api.create_folder("test")
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    @patch('src.network.query_model.Query.delete_node',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"getUserByEmail": "test"})
    def test_delete_node(self, mocked_info, mocked_response):
        api.client = gql.client.Client()
        api.delete_node("test")
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    def test_cookie2str_success(self):
        key = "ZM_AUTH_TOKEN"
        value = "mamma"
        result = api.cookie2str({key: value})
        self.assertEqual(result, key + "=" + value)

    def test_cookie2str_failure(self):
        key = "test"
        value = "mamma"
        result = api.cookie2str({key: value})
        self.assertEqual(result, "")

    def test_check_status_code_ok(self):
        test_obj = ApiTest.RequestObj()
        self.assertEqual(api.check_status_code(test_obj), None)

    def test_check_status_code_401(self):
        test_obj = ApiTest.RequestObj("test", 401)
        try:
            api.check_status_code(test_obj)
        except LoginError as e:
            self.assertEqual(str(e), str(LoginError()))

    def test_check_status_code_Error(self):
        test_obj = ApiTest.RequestObj("test", Status.Error)
        try:
            api.check_status_code(test_obj)
        except APIException as e:
            self.assertEqual(str(e), str(APIException()))

    @patch('requests.get', return_value=RequestObj())
    @patch('src.network.api.get_user_id', return_value="test")
    def test_download_node_from_server_ok(self, mocked_response, mocked_get_id):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated, self.path))
        self.assertEqual(api.download_node_from_server(test_node, self.path), None)
        mocked_response.assert_called_once()
        mocked_get_id.assert_called_once()
        file_path = os.path.join(self.path, self.file_name)
        self.assertEqual(os.path.exists(file_path), True)
        self.assertEqual(os.path.getmtime(file_path), updated)

    @patch('requests.get', return_value=RequestObj("test", Status.Error))
    @patch('src.network.api.get_user_id', return_value="test")
    def test_download_node_from_server_error(self, mocked_response, mocked_get_id):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated, self.path))
        try:
            api.download_node_from_server(test_node, self.path)
        except APIException as e:
            mocked_response.assert_called_once()
            mocked_get_id.assert_called_once()
            self.assertEqual(str(e), str(APIException()))

    @patch('requests.post', return_value=RequestObj("test", Status.Ok))
    @patch('src.network.api.get_user_id', return_value="test")
    def test_upload_success(self, mocked_response, mocked_get_id):
        # creo file da leggere, potrei mockare anche la call
        # di lettura ma questo risulta piu facile ed indolore anche
        # se molto brutto
        full_path = os.path.join(self.path, self.file_name)
        with open(full_path, "w"):
            pass
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated,
                                  full_path))
        self.assertEqual(api.upload_node_to_server(test_node), None)
        mocked_response.assert_called_once()
        mocked_get_id.assert_called_once()

    @patch('requests.post', return_value=RequestObj("test", Status.Ok))
    @patch('src.network.api.get_user_id', return_value="test")
    def test_upload_error(self, mocked_response, mocked_get_id):
        # creo file da leggere, potrei mockare anche la call
        # di lettura ma questo risulta piu facile ed indolore anche
        # se molto brutto
        full_path = os.path.join(self.path, self.file_name)
        with open(full_path, "w"):
            pass
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated,
                                  full_path))
        try:
            api.upload_node_to_server(test_node)
        except APIException as e:
            mocked_response.assert_called_once()
            mocked_get_id.assert_called_once()
            self.assertEqual(str(e), str(APIException()))

    @patch('src.network.api.is_logged', return_value=True)
    def test_login_already_logged_in(self, mocked_function):
        result = api.login("test", "test")
        mocked_function.assert_called_once()
        self.assertEqual(result, True)
