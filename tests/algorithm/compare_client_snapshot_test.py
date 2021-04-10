import unittest
from unittest.mock import patch

from src.algorithm import compare_client_snapshot
from src.algorithm.tree_comparator import Actions
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from tests import default_code

node_name = "CLIENT_NODE"


def _get_test_node():
    updated = 200
    created = 100
    return TreeNode(Node(node_name, "test",
                         Type.Folder, created, updated, "test"))


class ResultObj:
    def __init__(self, action, _lun: int = 0):
        self.result = {
            "action": action,
            "node": _get_test_node(),
            "path": "test"
        }
        self.lun = _lun

    # metodo usato per poter usare len(obj)
    def __len__(self):
        return self.lun

    # metodo usato per poter iterare sull'oggetto
    def __iter__(self):
        yield self.result


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

    @patch('src.algorithm.tree_builder.get_tree_from_node_id', return_value=_get_test_node())
    def test_get_id_from_path(self, mocked_fun):
        x = compare_client_snapshot.get_id_from_path(self.env_settings.value("sync_path"))
        mocked_fun.assert_called_once()
        self.assertEqual(x, node_name)
