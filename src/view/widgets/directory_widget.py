import os
from PySide6.QtWidgets import (QToolButton)
from PySide6.QtGui import (QIcon, QDesktopServices)
from PySide6.QtCore import (Qt, QSize, QTimer, Signal, QSettings, QUrl)
from src.model.widgets.directory import Directory


class Direcory_Widget(QToolButton):
    Sg_double_clicked = Signal()
    Sg_load_current_content = Signal()

    def __init__(self, dir: Directory):
        super(Direcory_Widget, self).__init__()

        self.env_settings = QSettings()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.check_double_click)

        self.Sg_double_clicked.connect(self.on_double_click)

        self.setAccessibleName('Directory')

        file_icon = QIcon('./icons/folder.svg')

        self.setIcon(file_icon)
        self.setIconSize(QSize(45, 45))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.name = dir.get_name()
        self.creation_date = dir.get_creation_date()
        self.last_modified_date = dir.get_last_modified_date()

        self.setText(self.name)
        # add fields to structure

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

    def on_double_click(self):
        sync_path = "" if self.env_settings.value("sync_path") is None else \
            self.env_settings.value("sync_path")
        path = os.path.join(sync_path, self.name)
        file_path = QUrl.fromUserInput(path)
        QDesktopServices.openUrl(file_path)
