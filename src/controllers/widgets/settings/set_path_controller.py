from PySide6.QtCore import (Slot, Signal)
from src.model.widgets.settings_model import SettingsModel


class SetPathController():

    def __init__(self, model: SettingsModel, parent=None):

        self.model = model

    @Slot()
    def Sl_show_file_dialog_result(self, value: str):
        self.model.set_path(value)
