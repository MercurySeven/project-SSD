import unittest
from unittest.mock import patch

from src.controllers.main_controller import MainController
from tests import default_code


class MainControllerTest(unittest.TestCase):

    def setUp(self) -> None:
        """Metodo che viene chiamato prima di ogni metodo"""
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.main_controller = None

    def tearDown(self):
        """Metodo che viene chiamato dopo ogni metodo"""
        default_code.tearDown(self.env_settings, self.restore_path)

    @patch('src.controllers.main_controller.QFileDialog.exec_', return_value=False)
    @patch('src.controllers.main_controller.QApplication.quit')
    def test_default_none_path(self, mock_1, mock_2):
        self.env_settings.setValue("sync_path", "")
        self.main_controller = MainController(default_code.app)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
