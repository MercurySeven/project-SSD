from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)

from src.model.main_model import MainModel
from src.view.widgets.settings.set_path_widget import SetPathWidget
from src.view.widgets.settings.set_policy_widget import SetPolicyWidget
from src.view.widgets.settings.set_quota_disk_widget import SetQuotaDiskWidget
from src.view.widgets.settings.set_profile_view import SetProfileView
from src.view.widgets.settings.set_sync_time_widget import SetSyncTimeWidget


class SettingsView(QWidget):

    def __init__(self, main_model: MainModel, parent=None):
        super(SettingsView, self).__init__(parent)
        self.setObjectName("Settings")
        # Titolo
        self.title = QLabel("Impostazioni", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        # Impostazioni Path
        self.set_path_widget = SetPathWidget(main_model.settings_model)
        # Impostazioni Policy
        self.set_policy_widget = SetPolicyWidget(main_model.settings_model)
        # Impostazioni finestra sync
        self.set_sync_time_widget = SetSyncTimeWidget(main_model.settings_model)
        # Impostazioni quota disco
        self.set_quota_disk_widget = SetQuotaDiskWidget(main_model.settings_model)

        self.set_profile_widget = SetProfileView(main_model.network_model)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.set_path_widget)
        layout.addWidget(self.set_policy_widget)
        layout.addWidget(self.set_sync_time_widget)
        layout.addWidget(self.set_quota_disk_widget)
        layout.addWidget(self.set_profile_widget)
        layout.addStretch()
        self.setLayout(layout)
