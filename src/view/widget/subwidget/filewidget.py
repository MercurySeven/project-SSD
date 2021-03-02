from PySide6.QtWidgets import (QPushButton, QHBoxLayout, QWidget)

from PySide.QtGui import (QLabel)
class FileWidget(QWidget):
    def __init__(self, name, creation_date, last_modified_date, type, size, status):
        super(FileWidget, self).__init__()
        self.name = QLabel(name, self)
        self.creation_date = QLabel(creation_date, self)
        self.last_modified_date = QLabel(last_modified_date, self)
        self.type = QLabel(type, self)
        self.size = QLabel(size, self)
        self.status = QLabel(status, self)
        self.structure = QHBoxLayout(self)
        # add fields to structure
        self.structure.addWidget(self.name)
        self.structure.addWidget(self.name)
        self.structure.addWidget(self.name)
        self.structure.addWidget(self.name)
        self.structure.addWidget(self.name)
        self.structure.addWidget(self.name)

