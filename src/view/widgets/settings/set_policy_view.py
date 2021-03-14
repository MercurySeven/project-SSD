from PySide6.QtWidgets import (
    QWidget, QLabel, QRadioButton, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import (Signal, Slot)

from network import Policy
from model.widgets import SettingsModel
from controllers.widgets.settings import SetPolicyController


class SetPolicyView(QWidget):

    Sg_policy_changed = Signal(Policy)

    def __init__(self,
                 model: SettingsModel,
                 controller: SetPolicyController,
                 parent=None):
        super(SetPolicyView, self).__init__(parent)

        self._model = model
        self._controller = controller

        self._titolo = QLabel()
        self._titolo.setText(
            "Seleziona la politica di gestione dei conflitti")
        self._titolo.setAccessibleName('Subtitle')

        self._client = QRadioButton("Client")
        self._manual = QRadioButton("Manuale")
        self.Sl_model_changed()

        layout = QVBoxLayout()
        layout.addWidget(self._titolo)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self._client)
        sub_layout.addWidget(self._manual)

        layout.addLayout(sub_layout)
        self.setLayout(layout)

        self._client.clicked.connect(lambda: self.Sl_client_checked())
        self._manual.clicked.connect(lambda: self.Sl_manual_checked())

        self._model.Sg_model_changed.connect(lambda: self.Sl_model_changed())
        self.Sg_policy_changed.connect(self._controller.Sl_change_policy)

    @Slot()
    def Sl_client_checked(self):
        if self._client.isChecked():
            self.Sg_policy_changed.emit(Policy.Client)

    @Slot()
    def Sl_manual_checked(self):
        if self._manual.isChecked():
            self.Sg_policy_changed.emit(Policy.Manual)

    @Slot()
    def Sl_model_changed(self):
        new_policy = self._model.get_policy()
        self._update_policy(new_policy)

    def _update_policy(self, policy: Policy):
        if policy == Policy.Manual:
            self._client.setChecked(False)
            self._manual.setChecked(True)
        else:
            self._client.setChecked(True)
            self._manual.setChecked(False)
