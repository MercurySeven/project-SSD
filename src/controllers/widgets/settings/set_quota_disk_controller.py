from PySide6.QtCore import Slot
from src.model.widgets.settings_model import SettingsModel
from src.view.widgets.settings.set_quota_disk_view import SetQuotaDiskView


class SetQuotaDiskController:

    def __init__(self, model: SettingsModel, view: SetQuotaDiskView):
        self._model = model
        self._view = view

        self._view.Sg_view_changed.connect(self.Sl_view_changed)

    @Slot()
    def Sl_view_changed(self):
        new_quota = self._view.dedicatedSpace.text()
        if self._model.get_quota_disco_raw() != int(new_quota):
            self._model.set_quota_disco(new_quota)
