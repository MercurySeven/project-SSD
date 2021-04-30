from PySide6.QtCore import (Signal, Slot)
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton)

from src.model.network_model import NetworkModel


class SetProfileView(QWidget):

    Sg_profile_logout = Signal()

    def __init__(self, model: NetworkModel, parent=None):
        super(SetProfileView, self).__init__(parent)
        self._model = model

        self.setAccessibleName("InfoBox")

        # Titolo
        self._titolo = QLabel('Profilo')
        self._titolo.setAccessibleName('Title2')

        self.username = QLabel()

        sub_layout_user = QHBoxLayout()
        sub_layout_user.addWidget(QLabel('Account:'))
        sub_layout_user.addWidget(self.username)
        sub_layout_user.addStretch()

        self.spaceLabel = QLabel(" ")

        # Pulsante logout
        self.logout_button = QPushButton('Logout')
        self.logout_button.setMaximumWidth(150)
        self.logout_button.clicked.connect(self.Sl_logout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.spaceLabel)
        self.buttonLayout.addWidget(self.logout_button)
        self.buttonLayout.addWidget(self.spaceLabel)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self._titolo)
        layout.addWidget(self.spaceLabel)
        layout.addLayout(sub_layout_user)
        layout.addLayout(self.buttonLayout)

        self.setLayout(layout)
        self.Sl_model_changed()

    @Slot()
    def Sl_model_changed(self):
        if self._model.is_logged:
            self.username.setText(self._model.get_username())

    @Slot()
    def Sl_logout(self):
        self.Sg_profile_logout.emit()
