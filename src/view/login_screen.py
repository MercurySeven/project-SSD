from PySide2.QtCore import (Signal, Slot, Qt)
from PySide2.QtWidgets import (QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog)

from src.model.network_model import NetworkModel
from src.view.stylesheets.qssManager import setQss


class LoginScreen(QDialog):

    Sg_login_success = Signal()
    Sg_login_failure = Signal()

    def __init__(self, model: NetworkModel, parent=None):
        super(LoginScreen, self).__init__(parent)

        # gestione modello
        self.model = model

        # inizializzazione layout
        self.layout = QVBoxLayout()

        # label e field
        self.login_title = QLabel(self)
        self.login_title.setText("Effettua l'accesso")
        self.login_title.setAccessibleName('LoginTitle')

        self.login_label = QLabel(self)
        self.login_label.setText('Username')
        self.login_label.setAccessibleName('LoginLabel')

        self.user_field = QLineEdit(self)

        self.psw_label = QLabel(self)
        self.psw_label.setText('Password')
        self.psw_label.setAccessibleName('LoginLabel')

        self.psw_field = QLineEdit(self)
        self.psw_field.setEchoMode(QLineEdit.Password)

        self.user_field.setText(self.model.get_username())

        # pulsante invio form
        self.login_button = QPushButton(self)
        self.login_button.setText('Login')

        # gestione layout
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.login_title)
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.user_field)
        self.layout.addWidget(self.psw_label)
        self.layout.addWidget(self.psw_field)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)
        setQss("./assets/style.qss", self)

    @Slot()
    def Sl_model_changed(self):
        is_logged = self.model.is_logged()
        if is_logged:
            self.Sg_login_success.emit()

    def get_user(self) -> str:
        return self.user_field.text()

    def get_psw(self) -> str:
        return self.psw_field.text()

    @Slot()
    def Sl_login_fail(self):
        self.Sg_login_failure.emit()
