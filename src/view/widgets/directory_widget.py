from PySide6.QtCore import (Qt, QSize, QTimer, Signal, Slot)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QToolButton)


class DirectoryWidget(QToolButton):
    Sg_double_clicked = Signal(str)

    def __init__(self):
        super(DirectoryWidget, self).__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.Sl_check_double_click)

        self.setAccessibleName('Directory')

        self.setIcon(QIcon('./assets/icons/Cartella.png'))
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    @Slot()
    def Sl_check_double_click(self):
        success = False
        if self.timer.isActive():
            time = self.timer.remainingTime()
            if time > 0:
                self.double_clicked_action()
                success = True
                self.timer.stop()
            if time <= 0:
                self.timer.start(250)

        if not self.timer.isActive() and not success:
            self.timer.start(250)

    def double_clicked_action(self) -> None:
        pass
