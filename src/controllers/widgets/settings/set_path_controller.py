from PySide6.QtCore import (Slot)
from src.model.widgets.settings_model import SettingsModel
from src.view.widgets.settings.set_path_view import SetPathView


class SetPathController:

    def __init__(self, model: SettingsModel, view: SetPathView):
        self._model = model
        self._view = view

        self._model.Sg_model_changed.connect(self._view.Sl_model_changed)
        self._view.Sg_view_changed.connect(self.Sg_view_changed)

    @Slot()
    def Sg_view_changed(self, value: str):
        if len(value) > 0:
            self._model.set_path(value)
