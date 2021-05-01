from src.controllers.file_controller import FileController
from src.model.main_model import MainModel
from src.view.file_view import FileView
from tests import default_code


class FileViewTest(default_code.DefaultCode):

    def setUp(self) -> None:
        super().setUp()

        self.main_model = MainModel()
        self.file_view_test = FileView(self.main_model.file_model)
        self.file_controller = FileController(self.main_model.file_model, self.file_view_test)

    def tearDown(self) -> None:
        super().tearDown()

    def test_defaults(self):
        """ Test file view test default values"""
        self.assertEqual(self.file_view_test.title.text(), "File sincronizzati")
        self.assertEqual(self.file_view_test.title.accessibleName(), "Title")
