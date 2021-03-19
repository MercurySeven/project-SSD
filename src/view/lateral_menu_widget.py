from PySide6.QtCore import (Qt, QSize)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QWidget)


class LateralMenuWidget(QWidget):

    def __init__(self, parent):
        super(LateralMenuWidget, self).__init__(parent)

        self.setAccessibleName('MenuNav')

        file_icon = QIcon('./icons/copy.png')
        settings_icon = QIcon('./icons/settings.png')

        self.files_button = QPushButton(self)
        self.files_button.setIcon(file_icon)
        self.files_button.setIconSize(QSize(30, 30))
        self.files_button.setCheckable(True)

        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(settings_icon)
        self.settingsButton.setIconSize(QSize(30, 30))
        self.settingsButton.setCheckable(True)
        self.files_button.setChecked(False)

        # layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.files_button)
        vbox.addStretch()
        vbox.addWidget(self.settingsButton)
        self.setLayout(vbox)
        self.files_button.setChecked(True)
