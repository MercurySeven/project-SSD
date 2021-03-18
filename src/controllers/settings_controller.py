from src.view.settings_widget import SettingsWidget
from src.model.widgets.settings_model import SettingsModel
from PySide6.QtCore import (Slot)
from src.network.policy import Policy


class SettingsController:
    def __init__(self, model: SettingsModel, view: SettingsWidget):
        self._model = model
        self._view = view

        self._model.Sg_model_changed.connect(view.set_policy_view.Sl_model_changed)
        self._view.set_policy_view.Sg_view_changed.connect(self.Sl_view_policy_changed)

        self._model.Sg_model_changed.connect(self._view.set_quota_disk_view.Sl_model_changed)
        self._view.set_quota_disk_view.Sg_view_changed.connect(self.Sl_view_quota_disk_changed)

        self._model.Sg_model_changed.connect(self._view.set_path_view.Sl_model_changed)
        self._view.set_path_view.Sg_view_changed.connect(self.Sg_set_path_view_changed)

    @Slot()
    def Sl_view_policy_changed(self):
        client = self._view.set_policy_view.client.isChecked()
        manual = self._view.set_policy_view.manual.isChecked()
        if client and not manual:
            self._model.set_policy(Policy.Client)
        elif manual and not client:
            self._model.set_policy(Policy.Manual)

    @Slot()
    def Sl_view_quota_disk_changed(self):
        new_quota = self._view.set_quota_disk_view.dedicatedSpace.text()
        if self._model.get_quota_disco_raw() != int(new_quota):
            self._model.set_quota_disco(new_quota)

    @Slot()
    def Sg_set_path_view_changed(self, value: str):
        if len(value) > 0:
            self._model.set_path(value)
