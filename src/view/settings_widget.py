from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)

from src.model.widgets.settings_model import SettingsModel
from src.view.widgets.settings.set_path_view import SetPathView
from src.view.widgets.settings.set_policy_view import SetPolicyView
from src.view.widgets.settings.set_quota_disk_view import SetQuotaDiskView


class SettingsWidget(QWidget):

    def __init__(self, model: SettingsModel, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.setObjectName("Settings")
        # Titolo
        self.title = QLabel("Impostazioni", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        # Impostazioni Path
        self.set_path_view = SetPathView(model)
        # Impostazioni Policy
        self.set_policy_view = SetPolicyView(model)
        # Impostazioni quota disco
        self.set_quota_disk_view = SetQuotaDiskView(model)


        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.set_path_view)
        layout.addWidget(self.set_policy_view)
        layout.addWidget(self.set_quota_disk_view)
        layout.addStretch()
        self.setLayout(layout)
