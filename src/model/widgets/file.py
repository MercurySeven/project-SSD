class File:
    def __init__(self,
                 name: str,
                 creation_date: str,
                 last_modified_date: str,
                 file_type: str,
                 size: str,
                 status: str):
        self._name = name
        self._creation_date = creation_date
        self._last_modified_date = last_modified_date
        self._file_type = file_type
        self._size = self._right_size(size)
        self._status = status

    def get_name(self) -> str:
        return self._name

    def get_creation_date(self) -> str:
        return self._creation_date

    def get_last_modified_date(self) -> str:
        return self._last_modified_date

    def get_type(self) -> str:
        return self._file_type

    def get_size(self) -> str:
        return str(self._size)

    def get_status(self) -> str:
        return self._status

    def set_name(self, name: str) -> None:
        self._name = name

    def set_creation_date(self, creation_date: str) -> None:
        self._creation_date = creation_date

    def set_last_modified_date(self, last_modified_date: str) -> None:
        self._last_modified_date = last_modified_date

    def set_type(self, _file_type: str) -> None:
        self._file_type = _file_type

    def set_size(self, size: int) -> None:
        self._size = self._right_size(size)

    def set_status(self, status: str) -> None:
        self._status = status

    def _right_size(self, size: str) -> str:
        if 3 < len(size) < 7:
            return size[:-3] + " KB"
        if 6 < len(size) < 9:
            return size[: -6] + " MB"
        if len(size) > 8:
            return size[: -8] + " GB"
        else:
            return size + " Byte"
