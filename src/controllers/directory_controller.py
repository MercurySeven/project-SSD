from src.model.widgets.directory import Directory
from src.view.widgets.directory_widget import Direcory_Widget
from PySide6.QtCore import (Slot)


class DirectoryController:
    def __init__(self, model: Directory, view: Direcory_Widget):
        self._model = model
        self._view = view
        self._view.Sg_double_clicked.connect(self.Sl_double_clicked)

    # TODO da completare doppio click
    @Slot()
    def Sl_double_clicked(self):
        print("si")
