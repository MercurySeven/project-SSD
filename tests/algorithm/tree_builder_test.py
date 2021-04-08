import os
import unittest

from src.algorithm import tree_builder
from src.algorithm.tree_builder import _build_tree_node
from src.model.algorithm.node import Type
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
        self.tree = _build_tree_node(self.file_name, "prova")
        self.assertEqual(self.tree.get_name(), "prova")
        payload = self.tree.get_payload()
        self.assertEqual(payload.path, self.file_name)
        self.assertEqual(payload.id, "CLIENT_NODE")
        self.assertEqual(payload.created_at, int(os.stat(self.file_name).st_ctime))
        self.assertEqual(payload.updated_at, int(os.stat(self.file_name).st_mtime))
        self.assertEqual(payload.type, Type.File)
