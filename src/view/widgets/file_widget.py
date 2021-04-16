from PySide6.QtWidgets import (QToolButton)
from PySide6.QtGui import (QIcon, QDesktopServices)
from PySide6.QtCore import (Qt, QSize, QTimer, Signal, Slot, QUrl)
from src.model.widgets.file import File


class FileWidget(QToolButton):
    Sg_double_clicked = Signal()

    def __init__(self, file: File):
        super(FileWidget, self).__init__()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.check_double_click)

        self.Sg_double_clicked.connect(self.Sl_on_double_click)

        self.setAccessibleName('File')

        self.setIcon(QIcon('./assets/icons/copy.png'))
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.name = file.get_name()
        self.creation_date = file.get_creation_date()
        self.last_modified_date = file.get_last_modified_date()
        self.type = file.get_type()
        self.size = file.get_size()
        self.status = file.get_status()
        self.path = file.get_path()

        self.setText(self.name)
        self.setToolTip(
            f"Nome: {self.name}\nUltima modifica: {self.last_modified_date}\nSize: {self.size}")

    def check_double_click(self):
        if self.timer.isActive():
            time = self.timer.remainingTime()
            if time > 0:
                self.Sg_double_clicked.emit()
            self.timer.stop()
            if time <= 0:
                self.timer.start(250)

        if self.timer.isActive() is False:
            self.timer.start(250)

    @Slot()
    def Sl_on_double_click(self):
        file_path = QUrl.fromUserInput(self.path)
        QDesktopServices.openUrl(file_path)
