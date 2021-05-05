
from tests import default_code
from src.view.widgets.directory_widget import DirectoryWidget


class DirectoryWidgetTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super().setUp()
        self.test_dir = DirectoryWidget()

    def tearDown(self) -> None:
        super().tearDown()
        self.test_dir.timer.stop()

    def test_check_double_click_success(self):
        self.test_dir.Sl_check_double_click()
        self.test_dir.Sl_check_double_click()
        test_result = self.test_dir.timer.isActive()
        self.assertEqual(test_result, False)

    def test_check_double_click_fail(self):
        self.test_dir.Sl_check_double_click()
        test_result = self.test_dir.timer.isActive()
        self.assertEqual(test_result, True)
