from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import (Slot, Qt, QPoint, QSize, Signal)

from src.model.widgets.remote_file import RemoteFile
from src.model.settings_model import SettingsModel
from src.view.widgets.file_widget import FileWidget
from src.view.stylesheets.qssManager import resource_path


class RemoteFileWidget(FileWidget):
    Sg_add_sync_file = Signal(str)
    Sg_remove_sync_file = Signal(str)

    def __init__(self, file: RemoteFile, settings: SettingsModel):
        super(RemoteFileWidget, self).__init__(file)
        self.settings_model = settings

        self.id = file.id
        self.file_size = file.get_size()
        self.last_editor = file.get_last_editor()

        self.Sl_on_file_status_changed()

    def contextMenuEvent(self, event) -> None:
        context_menu = QMenu(self)
        file_is_synced = self.settings_model.is_id_in_sync_list(self.id)

        # se il file non è syncato mostra aggiungi, altrimenti mostra rimuovi
        if file_is_synced is False:
            add_sync_action = context_menu.addAction("Aggiungi a sync")
        else:
            remove_sync_action = context_menu.addAction("Rimuovi da sync")

        # selezione voci menu
        if file_is_synced is False:
            action = context_menu.exec(self.mapToGlobal(event.pos()))
            if action == add_sync_action:
                self.Sg_add_sync_file.emit(self.id)
        else:
            action = context_menu.exec(self.mapToGlobal(event.pos()))
            if action == remove_sync_action:
                self.Sg_remove_sync_file.emit(self.id)

    def show_synced(self) -> None:
        p1 = QPixmap(self.icon().pixmap(self.icon().actualSize(QSize(1024, 1024))))
        p2 = QPixmap(resource_path('icons/KeepSync.png'))

        mode = QPainter.CompositionMode_SourceOver
        s = p1.size().expandedTo(p2.size())
        result = QPixmap(s)
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(QPoint(), p1)
        painter.setCompositionMode(mode)
        painter.drawPixmap(result.rect(), p2, p2.rect())
        painter.end()
        self.setIcon(QIcon(result))

    def _tooltip_builder(self, file_is_synced) -> str:
        tooltip = (f"Nome: {self.name}\n"
                   f"Ultima modifica: {self.last_modified_date}\n"
                   f"Dimensioni: {self.file_size}\n"
                   f"Ultimo editor: {self.last_editor}\n")

        tooltip += "Tieni aggiornato: " + ("Si" if file_is_synced else "No")
        self.setToolTip(tooltip)

    @Slot()
    def Sl_on_file_status_changed(self):
        file_is_synced = self.settings_model.is_id_in_sync_list(self.id)
        if file_is_synced:
            self.show_synced()
        else:
            self.set_icon()
        self._tooltip_builder(file_is_synced)
