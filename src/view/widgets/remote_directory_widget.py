from src.view.widgets.directory_widget import DirectoryWidget
from src.model.widgets.remote_directory import RemoteDirectory
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal

from src import settings


class RemoteDirectoryWidget(DirectoryWidget):
    Sg_add_sync_folder = Signal(str)
    Sg_remove_sync_folder = Signal(str)

    def __init__(self, dir: RemoteDirectory, parent=None):
        super(RemoteDirectoryWidget, self).__init__()
        self.parent = parent
        self.id = dir.get_id()
        self.name = dir.get_name()
        self.setText(self.name)
        if self.parent is not None:
            self.Sg_double_clicked.connect(self.parent.Sl_update_files_with_new_id)

    def contextMenuEvent(self, event) -> None:
        context_menu = QMenu(self)
        folder_is_synced = settings.id_is_in_sync_list(self.id)

        # se il folder non è syncato mostra aggiungi, altrimenti mostra rimuovi
        if folder_is_synced is False:
            add_sync_action = context_menu.addAction("Aggiungi a sync")
        else:
            remove_sync_action = context_menu.addAction("Rimuovi da sync")

        # selezione voci menu
        if folder_is_synced is False:
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == add_sync_action:
                self.Sg_add_sync_folder.emit(self.id)
        else:
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == remove_sync_action:
                self.Sg_remove_sync_folder.emit(self.id)

    def double_clicked_action(self) -> None:
        self.Sg_double_clicked.emit(self.id)
