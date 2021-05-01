from src.model.main_model import MainModel
from tests import default_code


class FileModelTest(default_code.DefaultCode):

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super().setUp()
        self.main_model = MainModel()
        self.model_test = self.main_model.file_model

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        super().tearDown()

    def test_get_data(self):
        print("============================= \n")
        x = self.model_test.get_data()
        print(x)
        print("============================= \n")
        # self.assertEquals(x, True)
