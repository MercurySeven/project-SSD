from src.algorithm import tree_comparator
from tests import default_code


class TreeComparatorTest(default_code.DefaultCode):

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
        file_name = ["ciao", "mamma"]
        first_folder_node = default_code._get_test_node()
        second_file_node = default_code._get_file_test_node(file_name[0])
        file_node = default_code._get_file_test_node(file_name[1])
        first_folder_node.add_node(file_node)
        first_folder_node.add_node(second_file_node)
        result = tree_comparator._compareFiles(first_folder_node, first_folder_node)
        # Empty list, nothing to do
        self.assertEquals(result, [])
