from src.model.main_model import MainModel
from src.view.login_screen import LoginScreen
from tests import default_code


class LoginScreenTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super().setUp()

        self.model = MainModel()
        self.login_test = LoginScreen(self.model.network_model)

    def tearDown(self) -> None:
        super().tearDown()

    def test_default(self):
        self.assertEqual(self.login_test.get_user(), self.login_test.model.get_username())
        self.assertEqual(self.login_test.get_psw(), self.login_test.model.get_password())
