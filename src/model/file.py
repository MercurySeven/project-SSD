class File:
    def __init__(self, name, creation_date, last_modified_date, type, size, status):
        self.__name = name
        self.__creation_date = creation_date
        self.__last_modified_date = last_modified_date
        self.__type = type
        self.__size = size
        self.__status = status

    def getName(self):
        return self.__name

    def getCreationDate(self):
        return self.__creation_date

    def getLastModifiedDate(self):
        return self.__last_modified_date

    def getType(self):
        return self.__type

    def getSize(self):
        return self.__size

    def getStatus(self):
        return self.__status

    def setName(self, name):
        self.__name = name


    def setCreationDate(self, creation_date):
        self.__creation_date = creation_date

    def setLastModifiedDate(self, last_modified_date):
        self.__last_modified_date = last_modified_date

    def setType(self, type):
        self.__type = type

    def setSize(self, size):
        self.__size = size

    def setStatus(self, status):
        self.__status = status