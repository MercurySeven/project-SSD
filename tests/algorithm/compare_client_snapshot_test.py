import unittest
from unittest.mock import patch

from src import settings
from src.algorithm import compare_client_snapshot
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.policy import Policy
from tests import default_code
from tests.default_code import _get_test_node, node_name, ResultObj


class CompareClientSnapshotTest(unittest.TestCase):

    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]

    def tearDown(self) -> None:
        default_code.tearDown(self.env_settings, self.restore_path)

    @patch('src.algorithm.tree_comparator.compareFolders', return_value="")
    def test_compare_snap_client_equal(self, mocked_fun):
        test_node = _get_test_node()
        compare_client_snapshot.compare_snap_client(test_node, test_node)
        mocked_fun.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.CLIENT_NEW_FOLDER, 1))
    @patch('src.algorithm.compare_client_snapshot.get_id_from_path')
    @patch('src.algorithm.os_handler.delete_node')
    def test_compare_snap_client_new_folder(self, mock_1, mock_2, mock_3):
        test_node = _get_test_node()
        compare_client_snapshot.compare_snap_client(test_node, test_node)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.CLIENT_NEW_FILE, 1))
    @patch('src.algorithm.compare_client_snapshot.get_id_from_path')
    @patch('src.algorithm.os_handler.delete_node')
    def test_compare_snap_client_new_file(self, mock_1, mock_2, mock_3):
        test_node = _get_test_node()
        compare_client_snapshot.compare_snap_client(test_node, test_node)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.SERVER_NEW_FOLDER, 1))
    @patch('src.algorithm.compare_client_snapshot.get_id_from_path')
    @patch('src.algorithm.os_handler.upload_folder')
    def test_compare_snap_client_server_new_folder(self, mock_1, mock_2, mock_3):
        test_node = _get_test_node()
        compare_client_snapshot.compare_snap_client(test_node, test_node)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.SERVER_NEW_FILE, 1))
    @patch('src.algorithm.compare_client_snapshot.get_id_from_path')
    @patch('src.algorithm.os_handler.upload_file')
    def test_compare_snap_client_server_new_file(self, mock_1, mock_2, mock_3):
        test_node = _get_test_node()
        compare_client_snapshot.compare_snap_client(test_node, test_node)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.SERVER_NEW_FILE, 1))
    @patch('src.algorithm.compare_client_snapshot.get_id_from_path')
    @patch('src.algorithm.os_handler.upload_file')
    def test_compare_snap_client_server_new_update_file(self, mock_1, mock_2, mock_3):
        test_node = _get_test_node()
        settings.update_policy(Policy.Client)
        compare_client_snapshot.compare_snap_client(test_node, test_node)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    @patch('src.algorithm.tree_builder.get_tree_from_node_id', return_value=_get_test_node())
    def test_get_id_from_path(self, mocked_fun):
        x = compare_client_snapshot.get_id_from_path(self.env_settings.value("sync_path"))
        mocked_fun.assert_called_once()
        self.assertEqual(x, node_name)
