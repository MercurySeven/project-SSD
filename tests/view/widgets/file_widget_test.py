import unittest

from src.model.file import File
from src.view.widgets.filewidget import FileWidget


class FileWidgetTest(unittest.TestCase):

    def setUp(self) -> None:
        self.file = File("nome", "creation date", "last mod date", "txt", "100", "status")
        self.file_view_test = FileWidget(self.file)

    def test_defaults(self):
        to_compare = "Ultima modifica: " + self.file.get_last_modified_date() + "\nSize: " + \
            self.file.get_size()
        self.assertEqual(self.file_view_test.toolTip(), to_compare)
        self.assertEqual(self.file_view_test.text(), self.file.get_name())
