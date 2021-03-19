import re

from PySide6 import QtCore
from PySide6.QtCore import (Signal, Slot)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget)

from src.model.model import Model
from src.model.widgets.sync_model import SyncModel
from src.view.stylesheets.qssManager import setQss
from src.view.widgets.sync_widget import SyncWidget
from .file_synchronized_widget import FileSyncronizedWidget
from .lateral_menu_widget import LateralMenuWidget
from .settings_view import SettingsView


class MainWindow(QMainWindow):
    """This is the main view class"""

    def __init__(self, model: Model):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SSD: Zextras Drive Desktop")
        self.setWindowIcon(QIcon("./icons/logo.png"))

        # widgets
        self.main_widget = MainWidget(model, self)

        # !! MainWindow must have a central widget !!
        self.setCentralWidget(self.main_widget)

        # style
        self.resize(1200, 800)

        setQss("style.qss", self)


class MainWidget(QWidget):
    # Signals
    Sg_switch_to_files = Signal()

    def __init__(self, model: Model, parent=None):

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
        self.sync_widget = SyncWidget(self._model.sync_model)
        self.menu_widget = LateralMenuWidget(self)
        self.files_widget = FileSyncronizedWidget(self._model.files_model, self)
        self.settings_view = SettingsView(self._model.settings_model, self)

        # stacked
        self.swidget = QStackedWidget()
        self.swidget.setAccessibleName("Stacked")
        self.swidget.addWidget(self.files_widget)
        self.swidget.addWidget(self.settings_view)

        # create layout
        self.menu_laterale = QVBoxLayout()
        self.menu_laterale.addWidget(self.sync_widget)
        self.menu_laterale.addWidget(self.menu_widget)
        self.menu_laterale.setSpacing(0)

        # self.central_view.addWidget(self.swidget)
        self.mainGrid.addLayout(self.menu_laterale)
        self.mainGrid.addLayout(self.central_view)
        # self.setLayout(self.mainGrid)
        # stylesheet
        for i in self.findChildren(QWidget, ):
            if re.findall("view", str(i)):
                i.setAttribute(QtCore.Qt.WA_StyledBackground, True)



    # metodo chiamato da lateral_menu_widget per scatenare il segnale
    # che arriva al modello per cambiare vista
    @Slot()
    def call_controller_for_list_file(self):
        self.Sg_switch_to_files.emit()


    def chage_current_window_to_files(self) -> None:
        self.swidget.setCurrentWidget(self.files_widget)
        self.menu_widget.settingsButton.setChecked(False)
        self.menu_widget.syncronizedButton.setChecked(True)

    @Slot()
    def update_view(self, list_of_files: dict, list_of_dirs: dict) -> None:
        self.files_widget.update_content(list_of_files, list_of_dirs)
        self.swidget.setCurrentWidget(self.syncronizedWidget)

    # def clear_layout(self, layout):
    #  for i in reversed(range(layout.count())):
    #     layout.itemAt(i).widget().setParent(None)
