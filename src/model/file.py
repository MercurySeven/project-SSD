class File:
    def __init__(self, name, creation_date, last_modified_date, type, size, status):
        self._name = name
        self._creation_date = creation_date
        self._last_modified_date = last_modified_date
        self._type = type
        self._size = self.right_size(size)
        self._status = status

    def get_name(self):
        return self._name

    def get_creation_date(self):
        return self._creation_date

    def get_last_modified_date(self):
        return self._last_modified_date

    def get_type(self):
        return self._type

    def get_size(self):
        return str(self._size)

    def get_status(self):
        return self._status

    def set_name(self, name):
        self._name = name

    def set_creation_date(self, creation_date):
        self._creation_date = creation_date

    def set_last_modified_date(self, last_modified_date):
        self._last_modified_date = last_modified_date

    def set_type(self, type):
        self._type = type

    def set_size(self, size):
        self._size = self.right_size(str(size))

    def set_status(self, status):
        self._status = status

    def right_size(self, str):
        if len(str)>3 and len(str)<7:
            return (str[:-3]+" KB")
        if len(str)>6 and len(str)<9:
            return (str[: -6]+ " MB")
        if len(str)>8:
            return (str[: -8]+ " GB")
        else: return (str+ " Byte")