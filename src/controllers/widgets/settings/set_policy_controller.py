from PySide6.QtCore import (QObject, Slot)
from network import Policy
from model.widgets import SettingsModel


class SetPolicyController(QObject):

    def __init__(self, model: SettingsModel, parent=None):
        super(SetPolicyController, self).__init__(parent)
        self.model = model

    @Slot(Policy)
    def Sl_change_policy(self, policy):
        self.model.set_policy(policy)
