import unittest

from PySide6.QtCore import QMargins

from src.model.widgets.file import File
from src.view.layouts.flowlayout import FlowLayout


class FlowLayoutTest(unittest.TestCase):

    def setUp(self) -> None:
        self.layout_test = FlowLayout()
        self.file1 = File("nome", "creation date", "last mod date", "txt", "100", "status")
        self.file2 = File("nome", "creation date", "last mod date", "txt", "100", "status")

    def test_defaults(self):
        """ Test default value of flow layout with parent"""
        self.assertEqual(self.layout_test.contentsMargins(), QMargins(0, 0, 0, 0))

    def test_add_item(self):
        """ Add two items and check if they are correctly in"""
        self.layout_test.addItem(self.file1)
        self.assertEqual(self.layout_test.itemAt(0), self.file1)
        self.layout_test.addItem(self.file2)
        self.assertEqual(self.layout_test.itemAt(1), self.file2)

    def test_count_item(self):
        """ Add two items and checks if count increases correctly"""
        self.assertEqual(self.layout_test.count(), 0)
        self.layout_test.addItem(self.file1)
        self.assertEqual(self.layout_test.count(), 1)
        self.layout_test.addItem(self.file2)
        self.assertEqual(self.layout_test.count(), 2)

    def test_take_at_with_two_item(self):
        """ add two items, remove one and checks if the second
        one is in the correct position"""
        self.layout_test.addItem(self.file1)
        self.layout_test.addItem(self.file2)
        self.assertEqual(self.layout_test.takeAt(0), self.file1)
        self.assertEqual(self.layout_test.itemAt(0), self.file2)

    def test_take_at_with_no_item(self):
        """ remove one item with array empty"""
        self.assertEqual(self.layout_test.takeAt(10), None)
