from src.model.file_model import FileModel
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel
from src.model.widgets.sync_model import SyncModel
from src.network.api import Api
from src.model.remote_file_model import RemoteFileModel


class MainModel:

    def __init__(self):
        self.file_model = FileModel.get_instance()
        self.settings_model = SettingsModel.get_instance()
        self.sync_model = SyncModel.get_instance()
        self.network_model: Api = NetworkModel.get_instance()
        self.remote_file_model = None

    def set_remote_file_model(self):
        self.remote_file_model = RemoteFileModel.get_instance(self.network_model)
