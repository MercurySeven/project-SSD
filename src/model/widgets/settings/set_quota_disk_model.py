from PySide6.QtCore import (QObject, Signal)
import settings
import math


class SetQuotaDiskModel(QObject):

    Sg_model_changed = Signal()

    def __init__(self):
        super(SetQuotaDiskModel, self).__init__(None)

    def get_quota_disco_raw(self) -> int:
        """Ritorna il valore grezzo"""
        return settings.get_quota_disco()

    def get_quota_disco(self) -> str:
        """Ritorna il valore con la sua unità adatta"""
        return self.convert_size(settings.get_quota_disco())

    def set_quota_disco(self, new_quota: str) -> None:
        settings.update_quota_disco(new_quota)
        self.Sg_model_changed.emit()

    @staticmethod
    def convert_size(size_bytes: int) -> str:
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
