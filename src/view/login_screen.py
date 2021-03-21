from PySide6.QtCore import (Signal, Slot, Qt)
from PySide6.QtWidgets import (QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog)

from src.model.network_model import NetworkModel
from src.view.stylesheets.qssManager import setQss


class LoginScreen(QDialog):

    Sg_login_success = Signal()

    def __init__(self, model: NetworkModel, parent=None):
        super(LoginScreen, self).__init__(parent)
        # gestione modello

        # inizializzazione layout
        self.layout = QVBoxLayout()
        self.model = model

        # label e filed

        self.loginTitle = QLabel(self)
        self.loginTitle.setText("Effettua l'accesso")
        self.loginTitle.setAccessibleName('LoginTitle')

        self.loginLabel = QLabel(self)
        self.loginLabel.setText('Username')
        self.loginLabel.setAccessibleName('LoginLabel')

        self.userField = QLineEdit(self)

        self.pswLabel = QLabel(self)
        self.pswLabel.setText('Password')
        self.pswLabel.setAccessibleName('LoginLabel')

        self.pswField = QLineEdit(self)
        self.pswField.setEchoMode(QLineEdit.Password)

        # pulsante invio form

        self.loginButton = QPushButton(self)
        self.loginButton.setText('Login')

        # gestione layout

        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.loginTitle)
        self.layout.addWidget(self.loginLabel)
        self.layout.addWidget(self.userField)
        self.layout.addWidget(self.pswLabel)
        self.layout.addWidget(self.pswField)
        self.layout.addWidget(self.loginButton)

        self.setLayout(self.layout)

        setQss("style.qss", self)

    @Slot()
    def Sl_model_changed(self):
        is_logged = self.model.is_logged()
        if is_logged:
            self.Sg_login_success.emit()
