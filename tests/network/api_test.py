import os
import pathlib
from unittest.mock import patch

import gql

from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import Status
from src.network.api_implementation import ApiImplementation
from src.network.api_exceptions import NetworkError, ServerError, APIException, LoginError
from tests import default_code
from tests.default_code import RequestObj, ResultObj


class ApiTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super().setUp()
        self.env_settings = super().get_env_settings()
        self.file_name = "test.txt"

        self.api = ApiImplementation()

        self.original_path = self.env_settings.value(super().SYNC_ENV_VARIABLE)

        self.path = os.path.join(self.original_path, "tree")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()
        to_remove = os.path.join(self.path, self.file_name)
        if os.path.exists(to_remove):
            try:
                os.remove(to_remove)
                os.rmdir(self.path)
            except PermissionError as e:
                print(e)

    @patch('requests.get', return_value=RequestObj("LoginScreen"))
    def test_is_logged_false(self, mocked_function):
        logged = self.api.is_logged()
        mocked_function.assert_called_once()
        self.assertFalse(logged)

    @patch('requests.get', return_value=RequestObj())
    def test_is_logged_true(self, mocked_function):
        logged = self.api.is_logged()
        mocked_function.assert_called_once()
        self.assertTrue(logged)

    def test_exception_handler_network_error(self):
        test_obj = RequestObj()
        try:
            test_obj.function_network_exception()
        except Exception as e:
            fun_name = "function_network_exception"
            exc_message = "test"

            self.assertEqual(str(e), str(NetworkError(f"{fun_name}: {exc_message}")))

    def test_exception_handler_server_error(self):
        test_obj = RequestObj()
        try:
            test_obj.function_server_exception()
        except Exception as e:
            self.assertEqual(str(e), str(ServerError()))

    def test_logout(self):
        self.assertTrue(self.api.logout())
        self.assertEqual(self.api.cookie, "")
        self.assertIsNone(self.api.client)

    @patch('gql.client.Client.__init__', return_value=None)
    def test_init_client(self, mocked_function):
        self.api.client = True
        self.assertTrue(self.api.client)
        self.api.init_client()
        mocked_function.assert_called_once()
        client = gql.client.Client()
        self.assertEqual(vars(self.api.client), vars(client))

    @patch('src.network.query_model.Query.get_info_from_email',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value=None)
    def test_get_info_from_email_exception_response_null(self, mocked_info, mocked_response):
        self.api.client = gql.client.Client()
        try:
            self.api.get_info_from_email()
        except Exception as e:
            self.assertEqual(str(e), str(ServerError("\'NoneType\' object is not subscriptable")))
        finally:
            mocked_info.assert_called_once()
            mocked_response.assert_called_once()

    @patch('src.network.query_model.Query.get_info_from_email',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"getUserByEmail": "test"})
    def test_get_info_from_email_success(self, mocked_info, mocked_response):
        self.api.init_client()
        self.assertEqual(self.api.get_info_from_email(), "test")
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    @patch('src.network.api_implementation.ApiImplementation.get_info_from_email',
           return_value={"id": "test"})
    def test_get_user_id(self, mocked_fun):
        self.api.user_id = ""
        self.assertEqual(self.api.get_user_id(), "test")
        mocked_fun.assert_called_once()

    @patch('src.network.query_model.Query.get_all_files',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"getUserByEmail": "test"})
    def test_get_content_from_node(self, mocked_info, mocked_response):
        self.api.client = gql.client.Client()
        self.assertEqual(self.api.get_content_from_node(), {"getUserByEmail": "test"})
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    @patch('src.network.query_model.Query.create_folder',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"createFolder": {"id": "test"}})
    def test_create_folder(self, mocked_info, mocked_response):
        self.api.client = gql.client.Client()
        self.api.create_folder("test")
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    @patch('src.network.query_model.Query.delete_node',
           return_value=[''' { hello }''', "b"])
    @patch('gql.client.Client.execute', return_value={"getUserByEmail": "test"})
    def test_delete_node(self, mocked_info, mocked_response):
        self.api.client = gql.client.Client()
        self.api.delete_node("test")
        mocked_info.assert_called_once()
        mocked_response.assert_called_once()

    def test_check_status_code_ok(self):
        test_obj = RequestObj()
        self.assertIsNone(self.api.check_status_code(test_obj))

    def test_check_status_code_401(self):
        test_obj = RequestObj("test", 401)
        try:
            self.api.check_status_code(test_obj)
        except LoginError as e:
            self.assertEqual(str(e), str(LoginError()))

    def test_check_status_code_Error(self):
        test_obj = RequestObj("test", Status.Error)
        try:
            self.api.check_status_code(test_obj)
        except APIException as e:
            self.assertEqual(str(e), str(APIException()))

    @patch('requests.get', return_value=RequestObj())
    @patch('src.network.api_implementation.ApiImplementation.get_user_id', return_value="test")
    @patch('src.network.api_implementation.ApiImplementation.get_content_from_node',
           return_value=ResultObj(1).id)
    def test_download_node_from_server_ok(self, mocked_1, mocked_2, mocked_3):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated, self.path))
        result = self.api.download_node(test_node, self.path, 10000)
        self.assertEquals(result[0], True)
        self.assertEqual(result[1], 'File downloaded')
        mocked_1.assert_called_once()
        mocked_2.assert_called_once()
        mocked_3.assert_called_once()
        file_path = os.path.join(self.path, self.file_name)
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.getmtime(file_path), updated)

    @patch('requests.get', return_value=RequestObj())
    @patch('src.network.api_implementation.ApiImplementation.get_user_id', return_value="test")
    @patch('src.network.api_implementation.ApiImplementation.get_content_from_node',
           return_value=ResultObj(1).id)
    def test_download_node_from_server_error_quota(self, mocked_response, mocked_get_id,
                                                   mocked_content):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated, self.path))
        result = self.api.download_node(test_node, self.path, 0)
        self.assertEquals(result[0], False)
        message = "Fallito il download del file %s, aumentare " \
                  "la quota disco o liberare spazio!" % self.file_name
        self.assertEquals(result[1], message)
        mocked_response.assert_called_once()
        mocked_get_id.assert_called_once()
        mocked_content.assert_called_once()
        file_path = os.path.join(self.path, self.file_name)
        self.assertEquals(os.path.exists(file_path), False)

    @patch('requests.get', return_value=RequestObj("test", Status.Error))
    @patch('src.network.api_implementation.ApiImplementation.get_user_id', return_value="test")
    @patch('src.network.api_implementation.ApiImplementation.get_content_from_node',
           return_value=ResultObj(1).id)
    def test_download_node_from_server_error(self, mocked_response, mocked_get_id, mocked_content):
        updated = 200
        created = 100
        test_node = TreeNode(Node("CLIENT_NODE", self.file_name,
                                  Type.Folder, created, updated, self.path))
        try:
            self.api.download_node(test_node, self.path, 100)
        except APIException as e:
            mocked_response.assert_called_once()
            mocked_get_id.assert_called_once()
            mocked_content.assert_called_once()
            self.assertEqual(str(e), str(APIException()))

    @patch('requests.post', return_value=RequestObj("test", Status.Ok))
    @patch('src.network.api_implementation.ApiImplementation.get_user_id', return_value="test")
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
        self.assertIsNone(self.api.upload_node(test_node))
        mocked_response.assert_called_once()
        mocked_get_id.assert_called_once()

    @patch('requests.post', return_value=RequestObj("test", Status.Ok))
    @patch('src.network.api_implementation.ApiImplementation.get_user_id', return_value="test")
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
            self.api.upload_node(test_node)
        except APIException as e:
            mocked_response.assert_called_once()
            mocked_get_id.assert_called_once()
            self.assertEqual(str(e), str(APIException()))

    @patch('src.network.api_implementation.requests.post', return_value=RequestObj("test", 401))
    def test_login_fail_login_exc(self, mock_1):
        try:
            self.api.login("test", "test")
        except LoginError as e:
            mock_1.assert_called_once()
            self.assertEqual(str(e), str(LoginError("Credenziali non valide")))

    @patch('src.network.api_implementation.requests.post', return_value=RequestObj("test", 500))
    def test_login_fail_server_exc(self, mock_1):
        try:
            self.api.login("test", "test")
        except ServerError as e:
            mock_1.assert_called_once()
            self.assertEqual(str(e), str(ServerError()))
