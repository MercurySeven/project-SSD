import time
import unittest
from unittest.mock import patch

from src.algorithm.decision_engine import DecisionEngine
from src.model.main_model import MainModel
from src.network.api_exceptions import APIException
from tests import default_code


class DecisionEngineTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = default_code.setUp()
        self.restore_path = tmp[0]
        self.env_settings = tmp[1]
        self.main_model = MainModel()
        self.decision_engine = DecisionEngine(self.main_model.network_model, True)

    def tearDown(self) -> None:
        default_code.tearDown(self.env_settings, self.restore_path)

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
    @patch('src.algorithm.compare_client_snapshot.compare_snap_client')
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
        mock_5.assert_called_once()
        mock_6.assert_called_once()

    @patch('src.algorithm.tree_builder.read_dump_client_filesystem', return_value="test")
    @patch('src.algorithm.tree_builder.get_tree_from_system', return_value="test")
    @patch('src.algorithm.compare_client_snapshot.compare_snap_client', side_effect=APIException())
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
