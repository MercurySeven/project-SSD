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
        self.__file_model = self.__file_model if \
            self.__file_model is not None else FileModel.create()
        self.__settings_model = self.__settings_model if \
            self.__settings_model is not None else SettingsModel.create()
        self.__sync_model = self.__sync_model if \
            self.__sync_model is not None else SyncModel.create()
        self.__network_model = self.__network_model if \
            self.__network_model is not None else NetworkModel.create()
        self.file_model = self.__file_model
        self.settings_model = self.__settings_model
        self.sync_model = self.__sync_model
        self.network_model = self.__network_model
