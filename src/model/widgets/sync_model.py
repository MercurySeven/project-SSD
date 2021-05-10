from PySide2.QtCore import (QObject, Signal)
from src import settings


class SyncModel(QObject):
    __model = None

    Sg_model_changed = Signal()

    __create_key = object()

    @classmethod
    def get_instance(cls):
        if SyncModel.__model is None:
            SyncModel.__model = SyncModel(cls.__create_key)
        return SyncModel.__model

    def __init__(self, create_key):
        assert (create_key == SyncModel.__create_key), \
            "SyncModel objects must be created using SyncModel.get_instance()"
        super(SyncModel, self).__init__(None)
        self.state = settings.get_is_synch()

    def set_state(self, new_state: bool):
        if self.state != new_state:
            self.state = new_state
            settings.update_is_sync(self.state)
            self.Sg_model_changed.emit()

    def get_state(self) -> bool:
        return self.state
