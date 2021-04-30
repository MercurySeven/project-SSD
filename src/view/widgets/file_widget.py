from PySide6.QtCore import (Qt, QSize, QTimer, Signal, Slot)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QToolButton)

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

        self.name = file.get_name()
        self.creation_date = file.get_creation_date()
        self.last_modified_date = file.get_last_modified_date()

        self.extension = self.get_extension()

        self.set_icon()
        self.setText(self.name)

        self.setText(self.name)

    def get_extension(self) -> str:
        e = self.name.split(".")
        return e[1]

    def set_icon(self):
        if self.extension == "txt":
            self.setIcon(QIcon('./assets/icons/Txt.png'))
            self.setIconSize(QSize(45, 45))
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if self.extension == "mp4":
            self.setIcon(QIcon('./assets/icons/Video.png'))
            self.setIconSize(QSize(45, 45))
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if (self.extension == "jpg") or (self.extension == "png"):
            self.setIcon(QIcon('./assets/icons/Immagine.png'))
            self.setIconSize(QSize(45, 45))
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if self.extension == "mp3":
            self.setIcon(QIcon('./assets/icons/Audio.png'))
            self.setIconSize(QSize(45, 45))
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

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
        pass
