from PySide6.QtCore import (Signal, Slot)
from PySide6.QtWidgets import (
    QWidget, QLabel, QRadioButton, QVBoxLayout)

from src.model.algorithm.policy import Policy
from src.model.settings_model import SettingsModel


class SetPolicyWidget(QWidget):

    Sg_view_changed = Signal()

    def __init__(self, model: SettingsModel, parent=None):
        super(SetPolicyWidget, self).__init__(parent)

        self._model = model

        self.setAccessibleName("InfoBox")

        self.titolo = QLabel("Politica di gestione conflitti")
        self.titolo.setAccessibleName('Title2')

        self.sottotitolo = QLabel("Cambia come vengono gestiti conflitti")
        self.sottotitolo.setAccessibleName('Sottotitolo')

        self.spaceLabel = QLabel(" ")

        self.client = QRadioButton(
            "Client: le modifiche in locale sovrascrivono quelle presenti nel server")
        self.manual = QRadioButton(
            "Manuale: verranno salvati entrambi i file, sarà l'utente a decidere cosa mantenere")
        self.Sl_model_changed()

        layout = QVBoxLayout()
        layout.addWidget(self.titolo)
        layout.addWidget(self.sottotitolo)
        layout.addWidget(self.spaceLabel)
        sub_layout = QVBoxLayout()
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
