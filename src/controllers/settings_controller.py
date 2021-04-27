import sys

from src.view.settings_view import SettingsView
from src.model.settings_model import SettingsModel
from src.model.network_model import NetworkModel
from src.model.main_model import MainModel
from PySide6.QtCore import (Slot)
from src.model.algorithm.policy import Policy
import bitmath


class SettingsController:
    def __init__(self, main_model: MainModel, view: SettingsView):
        self._sett_model: SettingsModel = main_model.settings_model
        self._net_model: NetworkModel = main_model.network_model
        self._view = view

        self._sett_model.Sg_model_changed.connect(view.set_policy_widget.Sl_model_changed)
        self._view.set_policy_widget.Sg_view_changed.connect(self.Sl_view_policy_changed)

        self._sett_model.Sg_model_changed.connect(self._view.set_quota_disk_widget.Sl_model_changed)
        self._view.set_quota_disk_widget.Sg_view_changed.connect(self.Sl_view_quota_disk_changed)

        self._sett_model.Sg_model_changed.connect(self._view.set_path_widget.Sl_model_changed)
        self._view.set_path_widget.Sg_view_changed.connect(self.Sg_set_path_widget_changed)

        self._net_model.Sg_model_changed.connect(self._view.set_profile_widget.Sl_model_changed)
        self._view.set_profile_widget.Sg_profile_logout.connect(self.Sl_view_profile_logout)

    @Slot()
    def Sl_view_policy_changed(self):
        client = self._view.set_policy_widget.client.isChecked()
        manual = self._view.set_policy_widget.manual.isChecked()
        if client and not manual:
            self._sett_model.set_policy(Policy.Client)
        elif manual and not client:
            self._sett_model.set_policy(Policy.Manual)

    @Slot()
    def Sl_view_quota_disk_changed(self):
        raw_quota = self._view.set_quota_disk_widget.dedicated_space.text()
        unit = self._view.set_quota_disk_widget.sizes_box.currentText()
        new_quota = "%s %s" % (raw_quota, unit)
        new_quota_to_byte = bitmath.parse_string(new_quota).to_Byte()
        old_quota = "%s %s" % (self._sett_model.get_quota_disco_raw(), "Byte")
        old_quota_to_byte = bitmath.parse_string(old_quota).to_Byte()
        if old_quota_to_byte != new_quota_to_byte:
            self._sett_model.set_quota_disco(new_quota_to_byte)

    @Slot()
    def Sl_view_profile_logout(self):
        self._net_model.logout()
        sys.exit()

    @Slot()
    def Sg_set_path_widget_changed(self, value: str):
        if len(value) > 0:
            self._sett_model.set_path(value)
