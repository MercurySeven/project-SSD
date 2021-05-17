from src.model.main_model import MainModel
from src.model.widgets.local_directory import LocalDirectory
from tests import default_code
import os


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
        # scendo di una directory
        self.model_test.current_folder = LocalDirectory(
            self.model_test.current_folder._node.get_children()[0],
            self.model_test.current_folder._node.get_children()[0].get_name())
        # eseguo get_data
        files, dirs = self.model_test.get_data()
        # costruisco una parent directory come nella funzione
        parent_directory = LocalDirectory(self.model_test.current_folder._node._parent, '..')
        # costruisco lista di file e cartelle
        test_files = self.model_test.current_folder._files
        test_dirs = self.model_test.current_folder._dirs
        # test di uguaglianza
        self.assertEqual(parent_directory._node, self.model_test.previous_folder._node)
        self.assertEqual(parent_directory._name, self.model_test.previous_folder._name)
        self.assertEqual(files, test_files)
        self.assertEqual(dirs, test_dirs)

    def test_get_data_root(self):
        # vado su root
        self.model_test.current_folder = LocalDirectory(
            self.model_test.current_folder._node._parent,
            self.model_test.current_folder._node._parent.get_name())
        # eseguo get_data
        files, dirs = self.model_test.get_data()
        # ricostruisco lista di file e cartelle
        test_files = self.model_test.current_folder._files
        test_dirs = self.model_test.current_folder._dirs
        # test di uguaglianza
        self.assertEqual(None, self.model_test.previous_folder)
        self.assertEqual(files, test_files)
        self.assertEqual(dirs, test_dirs)

    def test_set_current_node(self):
        # ottengo path
        path_to_set = self.model_test.current_folder._node.get_children()[0].get_payload().path
        # creo directory per testare ritorno
        test_target_directory = LocalDirectory(
            self.model_test.current_folder._node.get_children()[0],
            self.model_test.current_folder._node.get_children()[0].get_name())
        # eseguo set_current_node
        self.model_test.set_current_node(path_to_set)
        # test di uguaglianza
        self.assertEqual(
            self.model_test.current_folder._node.get_payload().path,
            test_target_directory._node.get_payload().path)
        self.assertEqual(self.model_test.current_folder._name, test_target_directory._name)

    def test_search_node_from_path(self):
        # vado su root
        if(self.model_test.current_folder._name != "ROOT"):
            self.model_test.current_folder = LocalDirectory(
                self.model_test.current_folder._node._parent,
                self.model_test.current_folder._node._parent.get_name())
        # ottengo nodo
        test_node = self.model_test.current_folder._node.get_children()[0]
        # ottengo path
        path_to_search = self.model_test.current_folder._node.get_children()[0].get_path()
        # chiamo search_node_from_path
        result_node = self.model_test.search_node_from_path(path_to_search)
        # test di uguaglianza
        self.assertEqual(test_node.get_path(), result_node.get_path())

    def test_search_node_from_path_path_does_not_exist(self):
        # vado su root
        if(self.model_test.current_folder._name != "ROOT"):
            self.model_test.current_folder = LocalDirectory(
                self.model_test.current_folder._node._parent,
                self.model_test.current_folder._node._parent.get_name())
        # ottengo nodo
        test_node = self.model_test.current_folder._node.get_children()[0]
        # ottengo path
        path_to_search = self.model_test.current_folder._node.get_children()[0].get_path()
        path_to_search = os.path.join(path_to_search, "FolderCheNonEsiste")
        print(path_to_search)
        # chiamo search_node_from_path
        result_node = self.model_test.search_node_from_path(path_to_search)
        # test di uguaglianza
        self.assertEqual(test_node.get_path(), result_node.get_path())

    def test_search_through_children(self):
        # vado su root
        if(self.model_test.current_folder._name != "ROOT"):
            self.model_test.current_folder = LocalDirectory(
                self.model_test.current_folder._node._parent,
                self.model_test.current_folder._node._parent.get_name())
        # ottengo nome
        name_to_search = self.model_test.current_folder._node.get_children()[0].get_name()
        # ottengo nodo
        node_to_search = self.model_test.current_folder._node
        # ottengo nodo obiettivo
        test_node = self.model_test.current_folder._node.get_children()[0]
        # chiamo _search_through_children
        result_node = self.model_test._search_through_children(name_to_search, node_to_search)
        # test di uguaglianza
        self.assertEqual(test_node.get_path(), result_node.get_path())

    def test_search_through_children_wrong_name(self):
        # vado su root
        if(self.model_test.current_folder._name != "ROOT"):
            self.model_test.current_folder = LocalDirectory(
                self.model_test.current_folder._node._parent,
                self.model_test.current_folder._node._parent.get_name())
        # ottengo nome
        name_to_search = "NomeCheNonEsiste"
        # ottengo nodo
        node_to_search = self.model_test.current_folder._node
        # chiamo _search_through_children
        result_node = self.model_test._search_through_children(name_to_search, node_to_search)
        # test di uguaglianza
        self.assertEqual(None, result_node)

    def test_clear_view(self):
        self.model_test.clear_view()
        self.assertEqual(self.model_test.current_folder._files, [])
        self.assertEqual(self.model_test.current_folder._dirs, [])
