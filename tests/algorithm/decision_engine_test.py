import time
from unittest.mock import patch

from src.algorithm.decision_engine import DecisionEngine
from src.algorithm.tree_comparator import Actions
from src.controllers.notification_controller import NotificationController
from src.model.main_model import MainModel
from src.network.api_exceptions import APIException, LoginError
from tests import default_code
from tests.default_code import ResultObj, _get_test_node


class DecisionEngineTest(default_code.DefaultCode):
    def setUp(self) -> None:
        super().setUp()
        self.env_settings = super().get_env_settings()
        self.main_model = MainModel()
        self.notif_controller = NotificationController(
            default_code.DefaultCode.app, ResultObj("test"))
        self.decision_engine = DecisionEngine(self.main_model, self.notif_controller, True)

    def tearDown(self) -> None:
        super().tearDown()

    def test_default(self):
        # Davide
        self.assertEqual(self.decision_engine.running, True)
        self.assertEqual("Algoritmo" in self.decision_engine.getName(), True)
        self.assertEqual(self.decision_engine.isDaemon(), True)

    def test_set_running(self):
        # Davide
        self.assertEqual(self.decision_engine.running, True)
        self.decision_engine.set_running(False)
        self.assertEqual(self.decision_engine.running, False)
        self.decision_engine.set_running(True)
        self.assertEqual(self.decision_engine.running, True)

    @patch('src.algorithm.tree_builder.read_dump_client_filesystem', return_value="test")
    @patch('src.algorithm.tree_builder.get_tree_from_system', return_value="test")
    @patch('src.algorithm.compare_snap_client.CompareSnapClient.check')
    @patch('src.algorithm.tree_builder.get_tree_from_node_id')
    @patch('src.algorithm.decision_engine.DecisionEngine.compute_decision')
    @patch('src.algorithm.tree_builder.dump_client_filesystem')
    def test_run_thread_success(self, mock_1, mock_2, mock_3, mock_4, mock_5, mock_6):
        # Attiva il thread
        self.decision_engine.start()

        time.sleep(0.5)
        self.decision_engine.set_running(False)
        # Aspetta che entri nell' if per poi mettere il booleano = False

        # Tutte le chiamate devono essere state effettuate, poichè
        # queste funzioni vengono chiamate se tutto va a buon fine
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()
        mock_4.assert_called_once()
        self.assertEqual(mock_5.call_count, 2)
        mock_6.assert_called_once()

    @patch('src.algorithm.tree_builder.read_dump_client_filesystem', return_value="test")
    @patch('src.algorithm.tree_builder.get_tree_from_system', return_value="test")
    @patch('src.algorithm.compare_snap_client.CompareSnapClient.check', side_effect=APIException())
    @patch('src.algorithm.tree_builder.get_tree_from_node_id')
    @patch('src.algorithm.decision_engine.DecisionEngine.compute_decision')
    @patch('src.algorithm.tree_builder.dump_client_filesystem')
    def test_run_thread_exception(self, mock_1, mock_2, mock_3, mock_4, mock_5, mock_6):
        # Attiva il thread
        self.decision_engine.start()

        time.sleep(0.5)
        self.decision_engine.set_running(False)
        # Aspetta che entri nell' if per poi mettere il booleano = False

        mock_6.assert_called_once()
        mock_5.assert_called_once()
        mock_4.assert_called_once()

        # Queste call non devono essere fatte, perchè se l'eccezione
        # è stata correttamente alzata allora queste funzioni non
        # vengono mai chiamate
        self.assertEqual(mock_1.call_count, 0)
        self.assertEqual(mock_2.call_count, 0)
        self.assertEqual(mock_3.call_count, 0)

    @patch('src.algorithm.tree_builder.read_dump_client_filesystem', return_value="test")
    def test_run_thread_false(self, mock_1):
        # Attiva il thread
        self.decision_engine.set_running(False)
        self.decision_engine.start()

        time.sleep(0.5)

        self.assertEqual(mock_1.call_count, 0)

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.CLIENT_NEW_FOLDER, 0))
    @patch('src.algorithm.os_handler.upload_folder')
    def test_compute_decision_new_client_folder_snap_false(self, mock_1, mock_2):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, False)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.CLIENT_NEW_FOLDER, 1))
    @patch('shutil.rmtree')
    def test_compute_decision_new_client_folder_snap_true(self, mock_1, mock_2):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.CLIENT_NEW_FILE, 1))
    @patch('src.algorithm.os_handler.upload_file')
    def test_compute_decision_new_client_file_snap_false(self, mock_1, mock_2):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, False)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.CLIENT_NEW_FILE, 1))
    @patch('os.remove')
    def test_compute_decision_new_client_file_snap_True(self, mock_1, mock_2):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.controllers.notification_controller.NotificationController.add_notification')
    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.SERVER_NEW_FOLDER, 1))
    @patch('src.algorithm.os_handler.download_folder',
           return_value=ResultObj(Actions.SERVER_NEW_FOLDER, 1))
    def test_compute_decision_new_server_folder(self, mock_1, mock_2, mock_3):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()
        mock_3.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.SERVER_NEW_FILE, 1))
    @patch('src.algorithm.os_handler.download_file')
    def test_compute_decision_new_server_file(self, mock_1, mock_2):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.algorithm.tree_comparator.compareFolders',
           return_value=ResultObj(Actions.SERVER_UPDATE_FILE, 1))
    @patch('src.algorithm.os_handler.download_file')
    def test_compute_decision_new_server_update_file(self, mock_1, mock_2):
        test_node = _get_test_node()
        self.decision_engine.compute_decision(test_node, test_node, True)
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('os.path.isdir', return_value=False)
    @patch('src.controllers.notification_controller.NotificationController.send_message')
    def test_check_isdir_false(self, mock_1, mock_2):
        self.decision_engine.check()
        mock_1.assert_called_once()
        mock_2.assert_called_once()

    @patch('src.controllers.notification_controller.NotificationController.send_message')
    @patch('src.algorithm.tree_builder.read_dump_client_filesystem',
           return_value="test")
    @patch('src.algorithm.tree_builder.get_tree_from_system',
           return_value="test")
    @patch('src.algorithm.compare_snap_client.CompareSnapClient.check',
           side_effect=LoginError(APIException))
    @patch('src.algorithm.tree_builder.get_tree_from_node_id')
    @patch('src.algorithm.decision_engine.DecisionEngine.compute_decision')
    @patch('src.algorithm.tree_builder.dump_client_filesystem')
    def test_run_thread_login_exception(
            self, mock_1, mock_2, mock_3, mock_4, mock_5, mock_6, mock_7):
        # Attiva il thread
        self.decision_engine.start()

        time.sleep(0.5)
        self.decision_engine.set_running(False)
        # Aspetta che entri nell' if per poi mettere il booleano = False

        mock_6.assert_called_once()
        mock_5.assert_called_once()
        mock_4.assert_called_once()
        mock_7.assert_called_once()

        # Queste call non devono essere fatte, perchè se l'eccezione
        # è stata correttamente alzata allora queste funzioni non
        # vengono mai chiamate
        self.assertEqual(mock_1.call_count, 0)
        self.assertEqual(mock_2.call_count, 0)
        self.assertEqual(mock_3.call_count, 0)
