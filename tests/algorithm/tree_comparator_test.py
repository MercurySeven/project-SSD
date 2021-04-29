from src.algorithm import tree_comparator
from src.algorithm.tree_comparator import Actions
from tests import default_code


class TreeComparatorTest(default_code.DefaultCode):
    FILE_NAME = ["ciao", "mamma"]

    def setUp(self):
        """Metodo che viene chiamato prima di ogni metodo"""
        super(TreeComparatorTest, self).setUp()

    def tearDown(self) -> None:
        super(TreeComparatorTest, self).tearDown()

    def test_get_only_files(self):
        file_name = ["ciao", "mamma"]
        folder_node = default_code._get_test_node()
        first_file_node = default_code._get_file_test_node(file_name[0])
        second_file_node = default_code._get_file_test_node(file_name[1])
        result = tree_comparator._get_only_files([folder_node,
                                                  first_file_node,
                                                  second_file_node])
        self.assertEquals([first_file_node, second_file_node], result)

    def test_get_only_folders(self):
        file_name = ["ciao", "mamma"]
        first_folder_node = default_code._get_test_node()
        second_file_node = default_code._get_file_test_node(file_name[0])
        file_node = default_code._get_file_test_node(file_name[1])
        result = tree_comparator._get_only_folders([first_folder_node,
                                                    second_file_node,
                                                    file_node])
        self.assertEquals([first_folder_node], result)

    def test_compare_files_equals(self):
        node = default_code.create_folder_with_files(self.FILE_NAME)
        result = tree_comparator._compareFiles(node, node)
        # Empty list, nothing to do
        self.assertEquals(result, [])

    def test_compare_files_client_new_file(self):
        # Imposto cartella server
        server_node = default_code.create_folder_with_files(self.FILE_NAME)
        # imposto cartella client
        client_node = default_code.create_folder_with_files(self.FILE_NAME)
        # Imposto file mancante
        missing_file = default_code._get_file_test_node()
        # Aggiungo file mancante
        client_node.add_node(missing_file)
        result = tree_comparator._compareFiles(client_node, server_node)
        # expected result
        exp_result = [{
            'node': missing_file,
            'id': 'CLIENT_NODE',
            'action': Actions.CLIENT_NEW_FILE}]

        self.assertEquals(result, exp_result)

    def test_compare_folders_equals(self):
        node = default_code.create_folder_with_folders(self.FILE_NAME)
        result = tree_comparator.compareFolders(node, node)
        # Empty list, nothing to do
        self.assertEquals(result, [])

    def test_compare_files_server_new_file(self):
        # Imposto cartella server
        server_node = default_code.create_folder_with_files(self.FILE_NAME)
        # imposto cartella client
        client_node = default_code.create_folder_with_files(self.FILE_NAME)
        # Imposto file mancante
        missing_file = default_code._get_file_test_node()
        # Aggiungo file mancante
        server_node.add_node(missing_file)
        result = tree_comparator._compareFiles(client_node, server_node)
        # expected result
        exp_result = [{
            'node': missing_file,
            'path': missing_file.get_payload().path,
            'action': Actions.SERVER_NEW_FILE}]

        self.assertEquals(result, exp_result)

    def test_compare_folders_client_new_folder(self):
        # Imposto cartella server
        server_node = default_code.create_folder_with_folders(self.FILE_NAME)
        # imposto cartella client
        client_node = default_code.create_folder_with_folders(self.FILE_NAME)
        # Imposto file mancante
        missing_file = default_code._get_test_node()
        # Aggiungo file mancante
        client_node.add_node(missing_file)
        result = tree_comparator.compareFolders(client_node, server_node)
        # expected result
        exp_result = [{
            'node': missing_file,
            'id': 'CLIENT_NODE',
            'action': Actions.CLIENT_NEW_FOLDER}]

        self.assertEquals(result, exp_result)

    def test_compare_folders_server_new_folder(self):
        # Imposto cartella server
        server_node = default_code.create_folder_with_folders(self.FILE_NAME)
        # imposto cartella client
        client_node = default_code.create_folder_with_folders(self.FILE_NAME)
        # Imposto file mancante
        missing_file = default_code._get_test_node()
        # Aggiungo file mancante
        server_node.add_node(missing_file)
        result = tree_comparator.compareFolders(client_node, server_node)
        # expected result
        exp_result = [{
            'node': missing_file,
            'path': missing_file.get_payload().path,
            'action': Actions.SERVER_NEW_FOLDER}]

        self.assertEquals(result, exp_result)
