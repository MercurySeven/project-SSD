from PySide6.QtCore import (QObject, Slot)
from src.model.widgets import SettingsModel


class SetPathController(QObject):

    def __init__(self, model: SettingsModel, parent=None):
        super(SetPathController, self).__init__(parent)

        self.model = model

    @Slot()
    def Sl_show_file_dialog_result(self, value: str):
        self.model.set_path(value)
