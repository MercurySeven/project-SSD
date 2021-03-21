from PySide6 import QtCore
from PySide6.QtCore import (Signal, Slot, QSize, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QDialog)

from src.view.stylesheets.qssManager import setQss

import re


class LoginScreen(QDialog):
    def __init__(self, parent=None):
        super(LoginScreen, self).__init__(parent)
        # gestione modello

        # inizializzazione layout
        self.layout = QVBoxLayout()

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

        #for i in self.findChildren(QWidget, ):
        #    if re.findall("view", str(i)):
        #        i.setAttribute(QtCore.Qt.WA_StyledBackground, True)