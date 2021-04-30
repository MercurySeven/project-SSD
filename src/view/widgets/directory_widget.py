from PySide6.QtWidgets import (QToolButton)
from PySide6.QtGui import (QIcon)
from PySide6.QtCore import (Qt, QSize, QTimer, Signal, Slot)


class DirectoryWidget(QToolButton):
    Sg_double_clicked = Signal(str)

    def __init__(self):
        super(DirectoryWidget, self).__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.Sl_check_double_click)

        self.setAccessibleName('Directory')

        self.setIcon(QIcon('./assets/icons/folder.png'))
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    @Slot()
    def Sl_check_double_click(self):
        pass
