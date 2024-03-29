import os
import pathlib
from unittest.mock import patch

from src.algorithm import tree_builder
from src.model.algorithm.node import Type, Node
from src.model.algorithm.tree_node import TreeNode
from src.model.main_model import MainModel
from tests import default_code
from tests.default_code import _get_default_dict, _get_tree_dict


class TreeBuilderTest(default_code.DefaultCode):
    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()
        self.env_settings = super().get_env_settings()

        self.original_path = self.env_settings.value(super().SYNC_ENV_VARIABLE)

        self.path = os.path.join(self.original_path, "tree")
        self.path = r'%s' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

        self.main_model = MainModel()
        self.model_test = self.main_model.network_model
        tree_builder.set_model(self.model_test)

        self.file_name = os.path.join(self.path, "prova.txt")
        with open(self.file_name, "w"):
            pass
        self.tree = tree_builder._build_tree_node(self.file_name, "ROOT")

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        try:
            os.remove(os.path.join(self.path, "prova.txt"))
        except Exception as e:
            print(e)
        super().tearDown()
        self._remove_dump()
        os.rmdir(self.path)

    def test_build_tree_node(self):
        node_name = "prova"
        self.tree = tree_builder._build_tree_node(self.path, node_name)
        updated = int(os.stat(self.path).st_mtime)
        created = int(os.stat(self.path).st_ctime)
        test_node = TreeNode(Node("CLIENT_NODE", node_name,
                                  Type.Folder, created, updated, self.path))
        self._test_tree_node(self.tree, test_node)

    @patch('os.path.exists', return_value=False)
    def test_build_tree_node_file_not_exists(self, m1):
        node_name = "prova"
        with self.assertRaises(FileNotFoundError):
            self.tree = tree_builder._build_tree_node(self.path, node_name)
            m1.assert_called_once()

    def test_get_tree_from_system(self):
        self.tree = tree_builder.get_tree_from_system(self.path)
        updated = int(os.stat(self.path).st_mtime)
        created = int(os.stat(self.path).st_ctime)
        test_node = TreeNode(Node("CLIENT_NODE", "ROOT", Type.Folder, created, updated, self.path))
        self._test_tree_node(self.tree, test_node)
        curr_dir_content = os.listdir(self.path)
        tree_childs = self.tree.get_children()
        tree_childs.reverse()

        for content in curr_dir_content:
            node = tree_childs.pop()
            file_path = os.path.join(self.path, content)
            created = int(os.stat(file_path).st_ctime)
            updated = int(os.stat(file_path).st_mtime)
            test_node = TreeNode(Node("CLIENT_NODE", content, Type.File,
                                      created, updated, file_path))
            self._test_tree_node(node, test_node)

    def test_create_node_from_dict(self):
        _dict = _get_default_dict()
        test_node = TreeNode(Node(_dict["id"], _dict["name"],
                                  Type.File, _dict["created_at"] / 1000,
                                  _dict["updated_at"] / 1000))
        node_to_test = tree_builder._create_node_from_dict(_dict)
        self._test_tree_node(node_to_test, test_node)

    def test_dump_and_read_client_filesystem(self):
        tree_builder.dump_client_filesystem(self.path)
        tree = tree_builder.read_dump_client_filesystem(self.path)

        self._remove_dump()

        tree_tester = tree_builder.get_tree_from_system(self.path)
        self._test_tree_node(tree, tree_tester)

    def test_read_nothing(self):
        tree = tree_builder.read_dump_client_filesystem(self.path)
        self.assertIsNone(tree)

    @patch('pickle.load', return_value=False)
    def test_read_with_exception(self, mocked_function):
        mocked_function.side_effect = Exception("test")
        tree_builder.dump_client_filesystem(self.path)
        tree = tree_builder.read_dump_client_filesystem(self.path)
        self.assertIsNone(tree)

    @patch('src.model.network_model.NetworkModel.get_content_from_node',
           return_value=_get_tree_dict())
    def test_get_tree_from_node_id(self, mocked_function):
        _dict = _get_default_dict()
        test_node = TreeNode(Node(_dict["id"], _dict["name"],
                                  Type.Folder, _dict["created_at"] / 1000,
                                  _dict["updated_at"] / 1000))
        node_to_test = tree_builder.get_tree_from_node_id("test")
        mocked_function.assert_called_once()
        self._test_tree_node(node_to_test, test_node)

    def test_create_hidden_folder_twice(self):
        hidden_folder = tree_builder._create_hidden_folder(self.path)
        pathing = os.path.join(self.path, tree_builder.FOLDER_NAME)
        self.assertEqual(hidden_folder, pathing)
        self.assertTrue(os.path.exists(pathing))
        self.assertTrue(os.path.isdir(pathing))
        hidden_folder = tree_builder._create_hidden_folder(self.path)
        self.assertEqual(hidden_folder, pathing)
        self.assertTrue(os.path.exists(pathing))
        self.assertTrue(os.path.isdir(pathing))

    def _remove_dump(self) -> None:
        pathing = os.path.join(self.path, tree_builder.FOLDER_NAME)
        client_dump = os.path.join(pathing, "client_dump.mer")
        if os.path.exists(client_dump):
            os.remove(client_dump)
        if os.path.exists(pathing):
            os.rmdir(pathing)

    def _test_tree_node(self, node_to_test: TreeNode, test_node: TreeNode):
        self.assertEqual(node_to_test.get_name(), test_node.get_name())
        payload_to_test = node_to_test.get_payload()
        test_payload = test_node.get_payload()
        self.assertEqual(payload_to_test.id, test_payload.id)
        self.assertEqual(payload_to_test.type, test_payload.type)
        self.assertEqual(payload_to_test.updated_at, test_payload.updated_at)
        self.assertEqual(payload_to_test.created_at, test_payload.created_at)
        self.assertEqual(payload_to_test.path, test_payload.path)
