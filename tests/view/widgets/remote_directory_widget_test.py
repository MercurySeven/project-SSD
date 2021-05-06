from tests import default_code
from src.view.widgets.remote_directory_widget import RemoteDirectoryWidget
from src.model.widgets.remote_directory import RemoteDirectory
from src.view.remote_file_view import RemoteFileView
from src.model.main_model import MainModel
from unittest.mock import patch

class RemoteDirectoryWidgetTest(default_code.DefaultCode):

    @patch(
        'src.algorithm.tree_builder.get_tree_from_node_id',
        return_value=default_code._get_test_node())
    def setUp(self, mocked) -> None:
        super().setUp()
        node = default_code.create_folder_with_files(["testFile"])
        base_dir = RemoteDirectory(node)
        self.test_model = MainModel()
        self.test_view = RemoteFileView(self.test_model)
        self.test_dir = RemoteDirectoryWidget(base_dir, self.test_view)

    def tearDown(self) -> None:
        super().tearDown()

    def test_double_clicked_action(self):
        self.test_dir.double_clicked_action()
