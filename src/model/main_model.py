from src.model.file_model import FileModel
from src.model.remote_file_model import RemoteFileModel
from src.model.settings_model import SettingsModel
from src.model.widgets.sync_model import SyncModel
from src.model.network_model import NetworkModel


class MainModel:

    def __init__(self):
        self.file_model: FileModel = FileModel.get_instance()
        self.remote_file_model: RemoteFileModel = RemoteFileModel.get_instance()
        self.settings_model: SettingsModel = SettingsModel.get_instance()
        self.sync_model: SyncModel = SyncModel.get_instance()
        self.network_model: NetworkModel = NetworkModel.get_instance()
