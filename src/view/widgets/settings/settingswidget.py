from PySide6.QtCore import (Signal, Slot, Qt, QSettings)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)

from .set_quota_disk_view import SetQuotaDiskView
from .set_path_view import SetPathView
from .set_policy_view import SetPolicyView
from model.widgets import SettingsModel
from controllers.widgets.settings import (
    SetPathController, SetPolicyController, SetQuotaDiskController)
import settings


class SettingsWidget(QWidget):

    # creating Signals
    Sg_dedicated_quota_changed = Signal()

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        self.setObjectName("Settings")

        # environment variables
        self.env_settings = QSettings()

        # Titolo
        self.title = QLabel("Impostazioni", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        # Impostazioni path
        self.settings_model = SettingsModel()
        self.set_path_controller = SetPathController(self.settings_model)
        self.set_path_view = SetPathView(
            self.settings_model, self.set_path_controller)

        # Impostazioni Priorità
        self.set_policy_controller = SetPolicyController(self.settings_model)
        self.set_policy_view = SetPolicyView(
            self.settings_model, self.set_policy_controller)

        # Impostazioni quota disco
        self.set_quota_disk_controller = SetQuotaDiskController(
            self.settings_model)
        self.set_quota_disk_view = SetQuotaDiskView(
            self.settings_model, self.set_quota_disk_controller)

        # Perchè questa roba?
        settings.check_file()

        # self.diskQuota.Sg_dedicated_quota_changed.connect(
        #     self.__Sl_dedicated_quota_changed)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.set_path_view)
        layout.addWidget(self.set_policy_view)
        layout.addWidget(self.set_quota_disk_view)
        layout.addStretch()
        self.setLayout(layout)

    # @Slot(int)
    # def __Sl_dedicated_quota_changed(self, new_size: int) -> None:
    #     # aggiorno la quota dedicata
    #     settings.update_quota_disco(str(new_size))
    #     # aggiorno il widget
    #     self.Sl_update_used_quota(self.diskQuota.get_used_quota())

    #     # avviso che la quota dedicata è cambiato
    #     self.Sg_dedicated_quota_changed.emit()

    # @Slot(int)
    # def Sl_update_used_quota(self, size: int) -> None:
    #     max_size = settings.get_quota_disco()
    #     # maxSize = self.env_settings.value("Disk/quota")
    #     self.diskQuota.set_context((0, max_size), size)
