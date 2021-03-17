from PySide6.QtCore import (QObject, Slot)
from src.network.policy import Policy
from src.model.widgets.settings_model import SettingsModel


class SetPolicyController(QObject):

    def __init__(self, model: SettingsModel, parent=None):
        super(SetPolicyController, self).__init__(parent)
        self.model = model

    @Slot(Policy)
    def Sl_change_policy(self, policy):
        self.model.set_policy(policy)
