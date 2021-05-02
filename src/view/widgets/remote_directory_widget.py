from src.view.widgets.directory_widget import DirectoryWidget
from src.model.widgets.remote_directory import RemoteDirectory


class RemoteDirectoryWidget(DirectoryWidget):

    def __init__(self, dir: RemoteDirectory, parent=None):
        super(RemoteDirectoryWidget, self).__init__()
        self.parent = parent
        self.id = dir.get_id()
        self.name = dir.get_name()
        self.setText(self.name)
        if self.parent is not None:
            self.Sg_double_clicked.connect(self.parent.Sl_update_files_with_new_id)

    def double_clicked_action(self) -> None:
        self.Sg_double_clicked.emit(self.id)
