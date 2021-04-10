import unittest
from src.model.algorithm.node import Node, Type


class TestNode(unittest.TestCase):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        self.node = Node("CLIENT_NODE", "Test", Type.File, 1000, 1022, "test/file.txt")
        self.folder = Node("CLIENT_NODE", "Test Folder", Type.Folder, 1000, 1022, "test")

    def test_id(self) -> None:
        self.assertEqual(self.node.id, "CLIENT_NODE")
        self.assertEqual(self.folder.id, "CLIENT_NODE")

    def test_name(self) -> None:
        self.assertEqual(self.node.name, "Test")
        self.assertEqual(self.folder.name, "Test Folder")

    def test_type(self) -> None:
        self.assertEqual(self.node.type, Type.File)
        self.assertEqual(self.folder.type, Type.Folder)

    def test_created_at(self) -> None:
        self.assertEqual(self.node.created_at, 1000)
        self.assertEqual(self.folder.created_at, 1000)

    def test_updated_at(self) -> None:
        self.assertEqual(self.node.updated_at, 1022)
        self.assertEqual(self.folder.updated_at, 1022)

    def test_path(self) -> None:
        self.assertEqual(self.node.path, "test/file.txt")
        self.assertEqual(self.folder.path, "test")


if __name__ == "__main__":
    unittest.main()
