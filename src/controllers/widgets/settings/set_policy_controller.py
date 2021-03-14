from PySide6.QtCore import (QObject, Slot)
from network import Policy
from model.widgets.settings import SetPolicyModel


class SetPolicyController(QObject):

    def __init__(self, model: SetPolicyModel, parent=None):
        super(SetPolicyController, self).__init__(parent)
        self.model = model

    @Slot(Policy)
    def Sl_change_policy(self, policy):
        self.model.set_policy(policy)
