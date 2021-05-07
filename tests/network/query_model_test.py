import unittest
from src.network.query_model import Query


class QueryModelTest(unittest.TestCase):

    def test_get_info_from_email(self) -> None:
        _, params = Query.get_info_from_email("a@a.it")
        result = {
            "email": "a@a.it"
        }
        self.assertEqual(result, params)

    def test_get_all_files(self) -> None:
        _, params = Query.get_all_files("ABCD")
        result = {
            "id": "ABCD"
        }
        self.assertEqual(result, params)

    def test_create_folder(self) -> None:
        _, params = Query.create_folder("ABCD", "cartella")
        result = {
            "parent_id": "ABCD",
            "name": "cartella"
        }
        self.assertEqual(result, params)

    def test_delete_node(self) -> None:
        _, params = Query.delete_node("ABCD")
        result = {
            "node_id": "ABCD"
        }
        self.assertEqual(result, params)


if __name__ == "__main__":
    unittest.main()
