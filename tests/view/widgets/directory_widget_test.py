
from tests import default_code
from src.view.widgets.directory_widget import DirectoryWidget
from src.view.widgets.local_directory_widget import LocalDirectoryWidget
from src.model.widgets.local_directory import LocalDirectory
# import time


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

    '''def test_check_double_click_fail_time(self):
        self.test_dir.Sl_check_double_click()
        time.sleep(0.250)
        self.test_dir.Sl_check_double_click()
        test_result = self.test_dir.timer.isActive()
        self.assertEqual(test_result, True)'''

    def test_double_clicked_action_exists(self):
        self.test_dir.double_clicked_action()

    def test_double_clicked_action_exists_local(self):
        test_dir = LocalDirectory(default_code._get_test_node())
        test_dir_widget = LocalDirectoryWidget(test_dir)
        test_dir_widget.double_clicked_action()
