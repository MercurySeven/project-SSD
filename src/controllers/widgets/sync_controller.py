from PySide6.QtCore import (Slot)
from src.model.widgets.sync_model import SyncModel
from src.view.widgets.sync_widget import SyncWidget


class SyncController:

    def __init__(self, model: SyncModel, view: SyncWidget):
        self._model = model
        self._view = view

        self._view.Sg_view_changed.connect(self.Sg_view_changed)
        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)

    @Slot()
    def Sg_view_changed(self):
        self._model.set_state(self._view.syncButton.isChecked())
