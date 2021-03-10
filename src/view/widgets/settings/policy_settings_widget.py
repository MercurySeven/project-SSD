from PySide6.QtWidgets import (
    QWidget, QProgressBar, QLabel, QVBoxLayout, QLineEdit)

from PySide6.QtCore import (QSettings, Signal, Slot)

from network import Policy


# TODO creare custom radiobutton
class PolicySettings(QWidget):

    Sg_policy_changed = Signal(Policy)

    def __init__(self, parent=None):
        super(PolicySettings, self).__init__(parent)