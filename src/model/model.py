from src.model.files_model import FilesModel
from src.model.widgets.settings_model import SettingsModel
from src.model.widgets.sync_model import SyncModel


class Model:
    def __init__(self):
        self.files_model = FilesModel()
        self.settings_model = SettingsModel()
        self.sync_model = SyncModel()

