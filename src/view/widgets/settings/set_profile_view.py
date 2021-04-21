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

        # Label nome utente

        sub_layout_user = QHBoxLayout()

        self.userLabel = QLabel()
        self.userLabel.setText('Username:')

        self.userName = QLabel()
        self.userName.setText('user')

        sub_layout_user.addWidget(self.userLabel)
        sub_layout_user.addWidget(self.userName)

        # Pulsante logout

        self.logoutButton = QPushButton()
        self.logoutButton.setText('Logout')

        self.logoutButton.clicked.connect(self.Sl_logout)

        # Layout

        layout = QVBoxLayout()

        layout.addWidget(self._titolo)
        layout.addLayout(sub_layout_user)
        layout.addWidget(self.logoutButton)

        self.setLayout(layout)

    @Slot()
    def Sl_model_changed(self):
        if self._model.is_logged:
            self.userName.setText(self._model.get_username())

    @Slot()
    def Sl_logout(self):
        self.Sg_profile_logout.emit()
