from PySide6.QtCore import (QSettings, Slot, Qt, Signal)
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QLabel, QPushButton)

from src.model.remote_file_model import RemoteFileModel
from src.model.main_model import MainModel
from src.model.settings_model import SettingsModel
from src.view.layouts.flowlayout import FlowLayout
from src.view.widgets.remote_directory_widget import RemoteDirectoryWidget
from src.view.widgets.remote_file_widget import RemoteFileWidget


class RemoteFileView(QWidget):
    Sg_update_files_with_new_id = Signal(str)
    Sg_add_sync_file = Signal(str)
    Sg_remove_sync_file = Signal(str)
    Sg_file_status_changed = Signal()

    def __init__(self, model: MainModel, parent=None):
        super(RemoteFileView, self).__init__(parent)

        self.env_settings = QSettings()
        self._model: RemoteFileModel = model.remote_file_model
        self.settings_model: SettingsModel = model.settings_model

        self.title = QLabel("File remoti", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.clicked.connect(self.Sl_refresh_button_clicked)
        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setAccessibleName("FileScroll")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        # contenitore per file
        self.fileWindow = QWidget(self)
        self.fileLayout = FlowLayout()
        self.fileLayout.setContentsMargins(0, 0, 0, 0)

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.refresh_button)

        layout = QVBoxLayout()
        layout.addLayout(header_layout)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.Sl_model_changed()

    @Slot()
    def Sl_model_changed(self) -> None:
        data = self._model.get_data()
        # Pulisco la vista
        for i in reversed(range(self.fileLayout.count())):
            self.fileLayout.itemAt(i).widget().setParent(None)
        # Se model.get_data ha avuto eccezioni di rete restituisce None
        if data is not None:
            list_of_files, list_of_dirs = data
            # Aggiungo le cartelle
            for i in list_of_dirs:
                self.fileLayout.addWidget(RemoteDirectoryWidget(i, self))
            # Aggiungo i file
            for i in list_of_files:
                self.fileLayout.addWidget(RemoteFileWidget(i, self.settings_model))
                self.fileLayout._item_list[-1].wid.Sg_add_sync_file.connect(self.Sl_add_sync_file)
                self.fileLayout._item_list[-1].wid.Sg_remove_sync_file.connect(
                    self.Sl_remove_sync_file)
                self.Sg_file_status_changed.connect(
                    self.fileLayout._item_list[-1].wid.Sl_on_file_status_changed)

    @Slot(str)
    def Sl_update_files_with_new_id(self, id: str) -> None:
        self.Sg_update_files_with_new_id.emit(id)

    @Slot()
    def Sl_refresh_button_clicked(self):
        self._model.folder_queue = ["LOCAL_ROOT"]
        self.Sl_model_changed()

    @Slot()
    def Sl_add_sync_file(self, id: str) -> None:
        self.Sg_add_sync_file.emit(id)

    @Slot()
    def Sl_remove_sync_file(self, id: str) -> None:
        self.Sg_remove_sync_file.emit(id)

    @Slot()
    def Sl_file_status_changed(self) -> None:
        self.Sg_file_status_changed.emit()
