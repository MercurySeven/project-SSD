from PySide6.QtCore import (QObject, Signal)
from network import Policy
import settings


class SetPolicyModel(QObject):

    Sg_model_changed = Signal()

    def __init__(self):
        super(SetPolicyModel, self).__init__(None)

    def get_policy(self) -> Policy:
        return Policy(settings.get_policy())

    def set_policy(self, new_policy: Policy) -> None:
        settings.update_policy(new_policy.value)
        self.Sg_model_changed.emit()
