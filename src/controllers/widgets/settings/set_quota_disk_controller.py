from PySide6.QtCore import (QObject, Slot)
from model.widgets.settings import SetQuotaDiskModel


class SetQuotaDiskController(QObject):

    def __init__(self, model: SetQuotaDiskModel, parent=None):
        super(SetQuotaDiskController, self).__init__(parent)
        self.model = model

    @Slot(int)
    def Sl_change_quota_disco(self, new_quota):
        self.model.set_quota_disco(str(new_quota))
