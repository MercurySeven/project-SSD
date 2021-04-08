import os
import unittest

from src.algorithm import tree_builder
from src.algorithm.tree_builder import _build_tree_node, get_tree_from_system
from src.algorithm.tree_builder import _create_node_from_dict
from src.model.algorithm.node import Type, Node
from src.model.algorithm.tree_node import TreeNode
from src.model.network_model import NetworkModel
from tests import default_code


class TreeBuilderTest(unittest.TestCase):
    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.model_test = NetworkModel()
        tree_builder.set_model(self.model_test)
        self.path = self.env_settings.value("sync_path")
        self.file_name = os.path.join(self.path, "prova.txt")
        with open(self.file_name, "w"):
            pass
        self.tree = _build_tree_node(self.file_name, "prova")

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        os.remove(os.path.join(self.path, "prova.txt"))
        default_code.tearDown(self.env_settings, self.restore_path)

    def test_build_tree_node(self):
        node_name = "prova"
        self.tree = _build_tree_node(self.path, node_name)
        updated = int(os.stat(self.path).st_mtime)
        created = int(os.stat(self.path).st_ctime)
        test_node = Node("CLIENT_NODE", node_name, Type.Folder, created, updated, self.path)
        self._test_node(self.tree, test_node)

    def test_get_tree_from_system(self):
        self.tree = get_tree_from_system(self.path)
        updated = int(os.stat(self.path).st_mtime)
        created = int(os.stat(self.path).st_ctime)
        test_node = Node("CLIENT_NODE", "ROOT", Type.Folder, created, updated, self.path)
        self._test_node(self.tree, test_node)
        curr_dir_content = os.listdir(self.path)
        tree_childs = self.tree.get_children()
        tree_childs.reverse()

        for content in curr_dir_content:
            node = tree_childs.pop()
            file_path = os.path.join(self.path, content)
            created = int(os.stat(file_path).st_ctime)
            updated = int(os.stat(file_path).st_mtime)
            test_node = Node("CLIENT_NODE", content, Type.File, created, updated, file_path)
            self._test_node(node, test_node)

    def test_create_node_from_dict(self):
        _id = "id"
        _name = "name"
        _type = "File"
        _created = 2000
        _updated = 2000
        test_node = Node(_id, _name, Type.File, _created / 1000, _updated / 1000)
        thisdict = {
            "id": _id,
            "name": _name,
            "type": _type,
            "created_at": _created,
            "updated_at": _updated
        }
        node_to_test = _create_node_from_dict(thisdict)
        self._test_node(node_to_test, test_node)

    def _test_node(self, node_to_test: TreeNode, test_node: TreeNode):
        self.assertEqual(node_to_test.get_name(), test_node.name)
        payload_to_test = node_to_test.get_payload()
        self.assertEqual(payload_to_test.id, test_node.id)
        self.assertEqual(payload_to_test.type, test_node.type)
        self.assertEqual(payload_to_test.updated_at, test_node.updated_at)
        self.assertEqual(payload_to_test.created_at, test_node.created_at)
        self.assertEqual(payload_to_test.path, test_node.path)
