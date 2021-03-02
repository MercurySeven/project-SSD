from PySide6.QtWidgets import (QHBoxLayout, QWidget, QLabel)
class FileWidget(QWidget):
    def __init__(self, name, creation_date, last_modified_date, type, size, status):
        super(FileWidget, self).__init__()
        self.name = QLabel(str(name), self)
        self.creation_date = QLabel(str(creation_date), self)
        self.last_modified_date = QLabel(str(last_modified_date), self)
        self.type = QLabel(str(type), self)
        self.size = QLabel(str(size), self)
        self.status = QLabel(str(status), self)
        self.structure = QHBoxLayout(self)
        # add fields to structure
        self.structure.addWidget(self.name)
        self.structure.addWidget(self.creation_date)
        self.structure.addWidget(self.last_modified_date)
        self.structure.addWidget(self.type)
        self.structure.addWidget(self.size)
        self.structure.addWidget(self.status)
        self.setLayout(self.structure)

