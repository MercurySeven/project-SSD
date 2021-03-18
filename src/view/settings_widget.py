from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)
from src.view.widgets.settings.set_quota_disk_view import SetQuotaDiskView
from src.view.widgets.settings.set_path_view import SetPathView
from src.view.widgets.settings.set_policy_view import SetPolicyView
from src.model.widgets.settings_model import SettingsModel
from src.controllers.widgets.settings.set_path_controller import SetPathController
from src.controllers.widgets.settings.set_policy_controller import SetPolicyController
from src.controllers.widgets.settings.set_quota_disk_controller import SetQuotaDiskController


class SettingsWidget(QWidget):

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        self.setObjectName("Settings")

        # Titolo
        self.title = QLabel("Impostazioni", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        # Impostazioni Path
        self.settings_model = SettingsModel()
        self.set_path_controller = SetPathController(self.settings_model)
        self.set_path_view = SetPathView(
            self.settings_model, self.set_path_controller)

        # Impostazioni Policy
        self.set_policy_view = SetPolicyView(self.settings_model)
        self.set_policy_controller = SetPolicyController(self.settings_model, self.set_policy_view)

        # Impostazioni quota disco
        self.set_quota_disk_controller = SetQuotaDiskController(
            self.settings_model)
        self.set_quota_disk_view = SetQuotaDiskView(
            self.settings_model, self.set_quota_disk_controller)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.set_path_view)
        layout.addWidget(self.set_policy_view)
        layout.addWidget(self.set_quota_disk_view)
        layout.addStretch()
        self.setLayout(layout)
