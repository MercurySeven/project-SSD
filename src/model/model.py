from src.model.files_model import FilesModel
from src.model.widgets.settings_model import SettingsModel


class Model:
    def __init__(self):
        self.file_window = FilesModel()
        self.settings_model = SettingsModel()
