from PySide6.QtWidgets import (
    QWidget, QLabel, QRadioButton, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import (Signal, Slot)

from src.network.policy import Policy
from src.model.widgets.settings_model import SettingsModel


class SetPolicyView(QWidget):

    Sg_view_changed = Signal()

    def __init__(self,
                 model: SettingsModel,
                 parent=None):
        super(SetPolicyView, self).__init__(parent)

        self._model = model

        self._titolo = QLabel()
        self._titolo.setText(
            "Seleziona la politica di gestione dei conflitti")
        self._titolo.setAccessibleName('Subtitle')

        self.client = QRadioButton("Client")
        self.manual = QRadioButton("Manuale")
        self.Sl_model_changed()

        layout = QVBoxLayout()
        layout.addWidget(self._titolo)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.client)
        sub_layout.addWidget(self.manual)

        layout.addLayout(sub_layout)
        self.setLayout(layout)

        self.client.clicked.connect(self.Sl_client_checked)
        self.manual.clicked.connect(self.Sl_manual_checked)

    @Slot()
    def Sl_client_checked(self):
        if self.client.isChecked():
            self.Sg_view_changed.emit()

    @Slot()
    def Sl_manual_checked(self):
        if self.manual.isChecked():
            self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        if self._model.get_policy() == Policy.Manual:
            self.client.setChecked(False)
            self.manual.setChecked(True)
        else:
            self.client.setChecked(True)
            self.manual.setChecked(False)
