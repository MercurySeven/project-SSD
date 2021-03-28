import unittest
from src.model.algorithm.node import Node, Type
from src.model.algorithm.tree_node import TreeNode


class TestTreeNode(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.files: list[Node] = [
            Node("CLIENT_NODE", "Test", Type.File, 1000, 1022, "root/file.txt"),
            Node("CLIENT_NODE", "Test2", Type.File, 1000, 1024, "root/file2.txt"),
            Node("CLIENT_NODE", "Test3", Type.File, 1000, 1026, "root/root2/file3.txt"),
        ]
        self.folders: list[Node] = [
            Node("CLIENT_NODE", "Test Folder", Type.Folder, 1000, 1022, "root"),
            Node("CLIENT_NODE", "Test Folder2", Type.Folder, 1000, 1025, "root/root2"),
        ]

        self.tree_node = TreeNode(self.folders[0])
        self.tree_node.add_node(TreeNode(self.files[0]))
        self.tree_node.add_node(TreeNode(self.files[1]))
        self.tree_node_sub = TreeNode(self.folders[1])
        self.tree_node_sub.add_node(TreeNode(self.files[2]))
        self.tree_node.add_node(self.tree_node_sub)

    def test_is_directory(self) -> None:
        self.assertTrue(self.tree_node.is_directory())
        self.assertFalse(self.tree_node._children[0].is_directory())
        self.assertFalse(self.tree_node._children[1].is_directory())
        self.assertTrue(self.tree_node._children[2].is_directory())
        self.assertFalse(self.tree_node._children[2]._children[0].is_directory())

    def test_get_name(self) -> None:
        tests = {
            "Test Folder": self.tree_node.get_name(),
            "Test": self.tree_node._children[0].get_name(),
            "Test2": self.tree_node._children[1].get_name(),
            "Test Folder2": self.tree_node._children[2].get_name(),
            "Test3": self.tree_node._children[2]._children[0].get_name()
        }
        for expected, values in tests.items():
            self.assertEqual(expected, values)

    def test_get_updated_at(self) -> None:
        self.assertEqual(1022, self.tree_node.get_updated_at())
        self.assertEqual(1022, self.tree_node._children[0].get_updated_at())
        self.assertEqual(1024, self.tree_node._children[1].get_updated_at())
        self.assertEqual(1025, self.tree_node._children[2].get_updated_at())
        self.assertEqual(1026, self.tree_node._children[2]._children[0].get_updated_at())

    def test_get_children(self) -> None:
        self.assertEqual(self.folders[0], self.tree_node.get_payload())
        self.assertEqual(self.files[0], self.tree_node._children[0].get_payload())
        self.assertEqual(self.files[1], self.tree_node._children[1].get_payload())
        self.assertEqual(self.folders[1], self.tree_node._children[2].get_payload())
        self.assertEqual(self.files[2], self.tree_node._children[2]._children[0].get_payload())

    def test_get_payload(self) -> None:
        self.assertEqual(3, len(self.tree_node.get_children()))
        self.assertEqual(self.files[2], self.tree_node._children[2]._children[0].get_payload())

    def test_parent(self) -> None:
        self.assertEqual(self.tree_node, self.tree_node._children[0]._parent)
        self.assertEqual(self.tree_node, self.tree_node._children[1]._parent)
        self.assertEqual(self.tree_node, self.tree_node._children[2]._parent)
        self.assertEqual(self.tree_node._children[2],
                         self.tree_node._children[2]._children[0]._parent)

    def test_add_node_exception(self) -> None:
        root = TreeNode(self.files[0])
        with self.assertRaises(ValueError):
            root.add_node(TreeNode(self.files[1]))


if __name__ == "__main__":
    unittest.main()
