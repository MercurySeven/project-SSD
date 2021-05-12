import re

from PySide6 import QtCore
from PySide6.QtCore import (Signal, Slot, QSize, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QPushButton, QLabel)

from src.model.main_model import MainModel
from src.view.stylesheets.qssManager import setQss, resource_path
from src.view.widgets.sync_widget import SyncWidget
from .file_view import FileView
from .remote_file_view import RemoteFileView
from .settings_view import SettingsView


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self, model: MainModel):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.setWindowIcon(QIcon(resource_path("./assets/icons/logo.png")))

        # widgets
        self.main_widget = MainWidget(model, self)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.main_widget)

        # style
        self.resize(1200, 800)

        setQss("./assets/style.qss", self)


class MainWidget(QWidget):

    Sg_switch_to_files = Signal()
    Sg_switch_to_remote = Signal()
    Sg_switch_to_settings = Signal()

    def __init__(self, model: MainModel, parent=None):

        super(MainWidget, self).__init__(parent)
        # gestione modello
        self._model = model

        # layouts
        # Grid di struttura dell'applicazione
        self.mainGrid = QHBoxLayout(self)
        self.mainGrid.setContentsMargins(0, 0, 0, 0)
        # finestra centrale in cui compariranno le opzioni selezionate
        self.central_view = QVBoxLayout()
        self.central_view.setSpacing(0)

        # widgets
        self.container_menu = QWidget(self)
        self.container_menu.setAccessibleName("MenuNav")

        self.sync_widget = SyncWidget(self._model.sync_model)

        self.files_button = QPushButton(self)
        self.files_button.setIcon(QIcon(resource_path("./assets/icons/Locali.png")))
        self.files_button.setIconSize(QSize(45, 45))
        self.files_button.setCheckable(True)

        self.remote_button = QPushButton(self)
        self.remote_button.setIcon(QIcon(resource_path("./assets/icons/Server.png")))
        self.remote_button.setIconSize(QSize(45, 45))
        self.remote_button.setCheckable(True)

        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon(resource_path("./assets/icons/settings.png")))
        self.settings_button.setIconSize(QSize(45, 45))
        self.settings_button.setCheckable(True)

        self.space = QLabel(" ")

        self.files_widget = FileView(self._model.file_model, self)
        self.remote_widget = RemoteFileView(self._model, self)
        self.settings_view = SettingsView(self._model, self)

        # stacked
        self.swidget = QStackedWidget()
        self.swidget.setAccessibleName("Stacked")
        self.swidget.addWidget(self.files_widget)
        self.swidget.addWidget(self.remote_widget)
        self.swidget.addWidget(self.settings_view)
        self.central_view.addWidget(self.swidget)

        # create layout
        self.menu_laterale = QVBoxLayout()
        self.menu_laterale.setContentsMargins(0, 0, 0, 0)
        self.menu_laterale.setAlignment(Qt.AlignCenter)
        self.menu_laterale.addWidget(self.sync_widget)
        self.menu_laterale.addWidget(self.files_button)
        self.menu_laterale.addWidget(self.space)
        self.menu_laterale.addWidget(self.remote_button)
        self.menu_laterale.addStretch()
        self.menu_laterale.addWidget(self.settings_button)
        self.menu_laterale.addWidget(self.space)
        self.menu_laterale.setSpacing(0)

        self.container_menu.setLayout(self.menu_laterale)

        self.mainGrid.addWidget(self.container_menu)
        self.mainGrid.addLayout(self.central_view)

        self.chage_current_view_to_files()

        self.files_button.clicked.connect(self.Sl_file_button_clicked)
        self.files_button.clicked.connect(self._model.file_model.Sl_update_model)
        self.remote_button.clicked.connect(self.Sl_remote_button_clicked)
        self.settings_button.clicked.connect(self.Sl_settings_button_clicked)

        # stylesheet
        for i in self.findChildren(QWidget, ):
            if re.findall("view", str(i)):
                i.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    # METODI PER CAMBIARE LA VISTA!!

    @Slot()
    def Sl_file_button_clicked(self):
        self.Sg_switch_to_files.emit()

    @Slot()
    def Sl_remote_button_clicked(self):
        self.Sg_switch_to_remote.emit()

    @Slot()
    def Sl_settings_button_clicked(self):
        self.Sg_switch_to_settings.emit()

    def chage_current_view_to_files(self) -> None:
        self.swidget.setCurrentWidget(self.files_widget)
        self.settings_button.setChecked(False)
        self.remote_button.setChecked(False)
        self.files_button.setChecked(True)

    def chage_current_view_to_remote(self) -> None:
        self.swidget.setCurrentWidget(self.remote_widget)
        self.settings_button.setChecked(False)
        self.remote_button.setChecked(True)
        self.files_button.setChecked(False)

    def chage_current_view_to_settings(self) -> None:
        self.swidget.setCurrentWidget(self.settings_view)
        self.settings_button.setChecked(True)
        self.remote_button.setChecked(False)
        self.files_button.setChecked(False)
