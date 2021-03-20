from PySide6.QtCore import (QObject, Signal)
from src import settings


class SyncModel(QObject):

    Sg_model_changed = Signal()

    def __init__(self):
        super(SyncModel, self).__init__(None)
        self.state = settings.get_is_synch()

    def set_state(self, new_state: bool):
        if self.state != new_state:
            self.state = new_state
            settings.update_is_sync(self.state)
            self.Sg_model_changed.emit()

    def get_state(self) -> bool:
        return self.state
