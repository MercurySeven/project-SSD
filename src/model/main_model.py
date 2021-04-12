from src.model.file_model import FileModel
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel
from src.model.widgets.sync_model import SyncModel
from src.network.api import Api


class MainModel:

    def __init__(self):
        self.file_model = FileModel.get_instance()
        self.settings_model = SettingsModel.get_instance()
        self.sync_model = SyncModel.get_instance()
        self.network_model: Api = NetworkModel.get_instance()
