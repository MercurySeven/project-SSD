class File:
    def __init__(self, name, creation_date, last_modified_date, type, size, status):
        self._name = name
        self._creation_date = creation_date
        self._last_modified_date = last_modified_date
        self._type = type
        self._size = size
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
        return self._size

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
        self._size = size

    def set_status(self, status):
        self._status = status
