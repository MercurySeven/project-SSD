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

        # connect to actions
        # qua va la chiamata solo per switchare di visuale
        # self.files_button.clicked.connect(self.parent().call_controller_for_list_file)
        # self.settingsButton.clicked.connect(self.showSettings)

        # layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.files_button)
        vbox.addStretch()
        vbox.addWidget(self.settingsButton)
        self.setLayout(vbox)
        self.files_button.setChecked(True)

   # def showSyncronized(self):
    #    self.parent().swidget.setCurrentWidget(self.parent().syncronizedWidget)
     #   self.settingsButton.setChecked(False)
      #  self.files_button.setChecked(True)

    # def showSettings(self):
     #   self.parent().swidget.setCurrentWidget(self.parent().settings_view)
      #  self.files_button.setChecked(False)
       # self.settingsButton.setChecked(True)
