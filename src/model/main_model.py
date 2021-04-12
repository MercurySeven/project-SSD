from src.model.file_model import FileModel
from src.model.network_model import NetworkModel
from src.model.settings_model import SettingsModel
from src.model.widgets.sync_model import SyncModel


class MainModel:
    __file_model = None
    __settings_model = None
    __sync_model = None
    __network_model = None

    def __init__(self):
        MainModel.__file_model = MainModel.__file_model if \
            MainModel.__file_model is not None else FileModel.create()
        MainModel.__settings_model = MainModel.__settings_model if \
            MainModel.__settings_model is not None else SettingsModel.create()
        MainModel.__sync_model = MainModel.__sync_model if \
            MainModel.__sync_model is not None else SyncModel.create()
        MainModel.__network_model = MainModel.__network_model if \
            MainModel.__network_model is not None else NetworkModel.create()
        self.file_model = MainModel.__file_model
        self.settings_model = MainModel.__settings_model
        self.sync_model = MainModel.__sync_model
        self.network_model = MainModel.__network_model
