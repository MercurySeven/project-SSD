import math
import os
from typing import Optional

import psutil
from PySide6.QtCore import (QObject, Signal, QSettings)

from src import settings
from src.model.algorithm.policy import Policy


class SettingsModel(QObject):
    Sg_model_changed = Signal()
    Sg_model_path_changed = Signal()
    __model = None

    __create_key = object()

    @classmethod
    def get_instance(cls):
        if SettingsModel.__model is None:
            SettingsModel.__model = SettingsModel(cls.__create_key)
        return SettingsModel.__model

    def __init__(self, create_key):
        assert (create_key == SettingsModel.__create_key), \
            "Network objects must be created using NetworkModel.create"
        super(SettingsModel, self).__init__(None)
        self.env_settings = QSettings()

    def get_policy(self) -> Policy:
        return Policy(settings.get_policy())

    def set_policy(self, new_policy: Policy) -> None:
        settings.update_policy(new_policy.value)
        self.Sg_model_changed.emit()

    def get_path(self) -> Optional[str]:
        return self.env_settings.value("sync_path")

    def set_path(self, new_path: str) -> None:
        self.env_settings.setValue("sync_path", new_path)
        self.env_settings.sync()
        self.Sg_model_changed.emit()
        self.Sg_model_path_changed.emit()

    def set_sync_time(self, new_sync_time: int) -> None:
        settings.update_sync_time(new_sync_time)
        self.Sg_model_changed.emit()

    def get_sync_time(self) -> Optional[int]:
        return settings.get_sync_time()

    def get_quota_disco_raw(self) -> int:
        """Ritorna il valore grezzo"""
        return settings.get_quota_disco()

    def get_quota_disco(self) -> str:
        """Ritorna il valore con la sua unità adatta"""
        return self.convert_size(settings.get_quota_disco())

    def set_quota_disco(self, new_quota: str) -> None:
        # trasforma new_quota scritto in mb in byte (non funziona)
        # quota = (int(new_quota) * 1024) ** 2
        # TODO: Il controllo non dovremmo farlo nel controller?
        mem = psutil.disk_usage('/')
        if self.get_size() <= int(new_quota) <= mem.free:
            settings.update_quota_disco(new_quota)
            self.Sg_model_changed.emit()

    @staticmethod
    def convert_size(size_bytes: int) -> str:
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_size(self) -> int:
        total_size = 0
        if not self.get_path():
            return 0
        for dirpath, dirnames, filenames in os.walk(self.get_path()):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size
