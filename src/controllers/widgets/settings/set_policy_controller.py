from PySide6.QtCore import Slot
from src.network.policy import Policy
from src.model.widgets.settings_model import SettingsModel
from src.view.widgets.settings.set_policy_view import SetPolicyView


class SetPolicyController:

    def __init__(self, model: SettingsModel, view: SetPolicyView):
        self._model = model
        self._view = view

        self._model.Sg_model_changed.connect(lambda: self._view.Sl_model_changed())
        self._view.Sg_view_changed.connect(self.Sl_change_view)

    @Slot()
    def Sl_change_view(self):
        client = self._view.client.isChecked()
        manual = self._view.manual.isChecked()
        if client and not manual:
            self._model.set_policy(Policy.Client)
        elif manual and not client:
            self._model.set_policy(Policy.Manual)
