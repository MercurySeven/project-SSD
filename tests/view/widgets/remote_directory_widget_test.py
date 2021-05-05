from tests import default_code
from src.view.widgets.remote_directory_widget import RemoteDirectoryWidget
from src.model.widgets.remote_directory import RemoteDirectory


class RemoteDirectoryWidgetTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super().setUp()
        node = default_code.create_folder_with_files(["testFile"])
        base_dir = RemoteDirectory(node)
        self.test_dir = RemoteDirectoryWidget(base_dir)

    def tearDown(self) -> None:
        super().tearDown()

    def test_double_clicked_action(self):
        self.test_dir.double_clicked_action()
