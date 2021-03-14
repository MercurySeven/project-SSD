from PySide6.QtCore import (QObject, Slot)
from model.widgets.settings import SetPathModel


class SetPathController(QObject):

    def __init__(self, model: SetPathModel, parent=None):
        super(SetPathController, self).__init__(parent)

        self.model = model

    @Slot()
    def Sl_show_file_dialog_result(self, value: str):
        self.model.set_path(value)
