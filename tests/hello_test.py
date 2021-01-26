import unittest
from src.hello import helloWorld


class TestHelloWorld(unittest.TestCase):
    def test_helloWorld(self) -> None:
        self.assertEqual(helloWorld(), "Hello World!")


if __name__ == "__main__":
    unittest.main()
