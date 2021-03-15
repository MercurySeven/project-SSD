from PySide6.QtCore import (QObject, Slot)
from src.model.widgets import SettingsModel


class SetQuotaDiskController(QObject):

    def __init__(self, model: SettingsModel, parent=None):
        super(SetQuotaDiskController, self).__init__(parent)
        self.model = model

    @Slot(int)
    def Sl_change_quota_disco(self, new_quota):
        if self.model.get_quota_disco_raw() != new_quota:
            self.model.set_quota_disco(str(new_quota))
