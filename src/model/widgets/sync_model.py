from PySide6.QtCore import (QObject, Signal)
from src import settings


class SyncModel(QObject):
    __has_already_run_once = False  # used to instantiate only one

    Sg_model_changed = Signal()

    __create_key = object()

    @classmethod
    def create(cls):
        if not SyncModel.__has_already_run_once:
            SyncModel.__has_already_run_once = True
            return SyncModel(cls.__create_key)

    def __init__(self, create_key):
        assert (create_key == SyncModel.__create_key), \
            "SyncModel objects must be created using NetworkModel.create"
        super(SyncModel, self).__init__(None)
        self.state = settings.get_is_synch()

    def set_state(self, new_state: bool):
        if self.state != new_state:
            self.state = new_state
            settings.update_is_sync(self.state)
            self.Sg_model_changed.emit()

    def get_state(self) -> bool:
        return self.state
