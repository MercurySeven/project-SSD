from PySide6.QtWidgets import (QToolButton)
from PySide6.QtGui import (QIcon)
from PySide6.QtCore import (Qt, QSize, QTimer, Signal, Slot)
from src.model.widgets.directory import Directory


class DirectoryWidget(QToolButton):
    Sg_double_clicked = Signal(str)

    def __init__(self, dir: Directory, parent=None):
        super(DirectoryWidget, self).__init__()
        self.parent = parent
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.Sl_check_double_click)

        self.setAccessibleName('Directory')

        self.setIcon(QIcon('./assets/icons/folder.png'))
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.name = dir.get_name()
        self.setText(self.name)

        # if self.parent is not None:
        #    self.Sg_double_clicked.connect(self.parent.Sl_update_files_with_new_path)
        # add fields to structure

    @Slot()
    def Sl_check_double_click(self):
        pass
