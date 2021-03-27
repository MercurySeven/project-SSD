from .difflibparser import DifflibParser


class DiffModel():
    def __init__(self, file_left_path: str, file_right_path: str):

        self.is_text_file = True
        try:
            with open(file_left_path, "r", encoding="utf-8") as fh:
                self.file_left = fh.read()

            with open(file_right_path, "r", encoding="utf-8") as fh:
                self.file_right = fh.read()
        except UnicodeDecodeError:
            self.is_text_file = False

    def getDiff(self) -> list:
        return DifflibParser(self.file_left.splitlines(), self.file_right.splitlines())

    def is_text_file(self) -> bool:
        return self.is_text_file
