import unittest
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode
from src.model.widgets.remote_file import RemoteFile


class RemoteFileTest(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        node = Node("ABCD", "FileRemoto.txt", Type.File, 2324,
                    2324, size=345, last_editor="a@a.it")
        self.remotefile = RemoteFile(TreeNode(node))

    def test_get_size(self) -> None:
        result = self.remotefile.get_size()
        self.assertEqual(result, "345.0 Byte")

    def test_get_last_editor(self) -> None:
        result = self.remotefile.get_last_editor()
        self.assertEqual(result, "a@a.it")


if __name__ == "__main__":
    unittest.main()
