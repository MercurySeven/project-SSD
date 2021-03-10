from PySide6.QtCore import (QObject, Slot, QSettings)
from network import (MetaData, Policy)
from view.widgets.settings import PolicySettings


class PolicyController(QObject):

    def __init__(self, widget: PolicySettings, model: MetaData, parent=None):
        super(PolicyController, self).__init__(parent)

        self.policy_settings = widget
        self.algorithm = model

        self.policy_settings.Sg_policy_changed.connect(self.Sl_change_policy)

    @Slot(Policy)
    def Sl_change_policy(self, policy):

        # TODO utilizzare Policy nel segnale

        if policy == "Client":
            self.algorithm.change_policy(Policy.Client)
        elif policy == "Server":
            self.algorithm.change_policy(Policy.Server)
        elif policy == "lastUpdate":
            self.algorithm.change_policy(Policy.lastUpdate)
        else:
            print("invalid policy")