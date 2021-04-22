from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton)
from PySide6.QtCore import (Signal, Slot)

from src.model.network_model import NetworkModel


class SetProfileView(QWidget):

    Sg_profile_logout = Signal()

    def __init__(self, model: NetworkModel, parent=None):
        super(SetProfileView, self).__init__(parent)
        self._model = model

        # Titolo
        self._titolo = QLabel()
        self._titolo.setText('Profilo')
        self._titolo.setAccessibleName('Subtitle')

        self.username = QLabel()

        sub_layout_user = QHBoxLayout()
        sub_layout_user.addWidget(QLabel('Username:'))
        sub_layout_user.addWidget(self.username)
        sub_layout_user.addStretch()

        # Pulsante logout
        self.logout_button = QPushButton('Logout')
        self.logout_button.clicked.connect(self.Sl_logout)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self._titolo)
        layout.addLayout(sub_layout_user)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)
        self.Sl_model_changed()

    @Slot()
    def Sl_model_changed(self):
        if self._model.is_logged:
            self.username.setText(self._model.get_username())

    @Slot()
    def Sl_logout(self):
        self.Sg_profile_logout.emit()
