import math
import os
from typing import Optional

import psutil
from PySide6.QtCore import (QObject, Signal, QSettings)
import bitmath

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
            "Settings objects must be created using NetworkModel.create"
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

    def get_sync_time(self) -> int:
        return settings.get_sync_time()

    def get_quota_disco_raw(self) -> float:
        """Ritorna il valore grezzo"""
        return settings.get_quota_disco()

    def get_quota_disco(self) -> str:
        """Ritorna il valore con la sua unità adatta"""
        return self.convert_size(settings.get_quota_disco())

    def set_quota_disco(self, new_quota: bitmath.Byte) -> None:
        # TODO: Il controllo non dovremmo farlo nel controller?
        folder_size = bitmath.parse_string(self.convert_size(self.get_size()))
        free_disk = bitmath.parse_string(self.convert_size(self.get_free_disk()))
        # Controllo che la nuova quota sia minore dello spazio disponibile nell'hdd
        # e maggiore dello spazio utilizzato dalla cartella corrente
        if folder_size <= new_quota <= free_disk:
            settings.update_quota_disco(str(new_quota.value))
            self.Sg_model_changed.emit()

    def get_free_disk(self) -> int:
        mem = psutil.disk_usage('/')
        return mem.free

    @staticmethod
    def convert_size(size_bytes: int) -> str:
        if size_bytes == 0:
            return "0 B"
        size_name = ("Byte", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_quota_libera(self) -> float:
        return self.get_quota_disco_raw() - self.get_size()

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

    def is_id_in_sync_list(self, id: str) -> bool:
        return id in settings.get_sync_list()

    def add_id_to_sync_list(self, id: str) -> None:
        """Aggiungi id a whitelist"""
        id_list = settings.get_sync_list()
        if not self.is_id_in_sync_list(id):
            id_list.append(id)
            settings.update_sync_list(id_list)
            self.Sg_model_changed.emit()

    def remove_id_from_sync_list(self, id: str) -> None:
        """Rimuovi id da whitelist"""
        id_list = settings.get_sync_list()
        if self.is_id_in_sync_list(id):
            id_list.remove(id)
            settings.update_sync_list(id_list)
            self.Sg_model_changed.emit()
