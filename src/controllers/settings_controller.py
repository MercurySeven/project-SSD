from src.view.settings_view import SettingsView
from src.model.settings_model import SettingsModel
from src.model.network_model import NetworkModel
from PySide6.QtCore import (Slot)
from src.model.algorithm.policy import Policy


class SettingsController:
    def __init__(self, model: SettingsModel, net_model: NetworkModel, view: SettingsView):
        self._model = model
        self._net_model = net_model
        self._view = view

        self._model.Sg_model_changed.connect(view.set_policy_widget.Sl_model_changed)
        self._view.set_policy_widget.Sg_view_changed.connect(self.Sl_view_policy_changed)

        self._model.Sg_model_changed.connect(self._view.set_quota_disk_widget.Sl_model_changed)
        self._view.set_quota_disk_widget.Sg_view_changed.connect(self.Sl_view_quota_disk_changed)

        self._model.Sg_model_changed.connect(self._view.set_path_widget.Sl_model_changed)
        self._view.set_path_widget.Sg_view_changed.connect(self.Sg_set_path_widget_changed)

        self._net_model.Sg_model_changed.connect(self._view.set_profile_widget.Sl_model_changed)
        self._view.set_profile_widget.Sg_profile_logout.connect(self.Sl_view_profile_logout)

    @Slot()
    def Sl_view_policy_changed(self):
        client = self._view.set_policy_widget.client.isChecked()
        manual = self._view.set_policy_widget.manual.isChecked()
        if client and not manual:
            self._model.set_policy(Policy.Client)
        elif manual and not client:
            self._model.set_policy(Policy.Manual)

    @Slot()
    def Sl_view_quota_disk_changed(self):
        new_quota = self._view.set_quota_disk_widget.dedicated_space.text()
        if self._model.get_quota_disco_raw() != int(new_quota):
            self._model.set_quota_disco(new_quota)

    @Slot()
    def Sl_view_profile_logout(self):
        self._net_model.logout()
        print('logging out')

    @Slot()
    def Sg_set_path_widget_changed(self, value: str):
        if len(value) > 0:
            self._model.set_path(value)
