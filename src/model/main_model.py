from src.model.file_model import FileModel
from src.model.widgets.settings_model import SettingsModel
from src.model.widgets.sync_model import SyncModel


class MainModel:
    def __init__(self):
        self.file_model = FileModel()
        self.settings_model = SettingsModel()
        self.sync_model = SyncModel()
