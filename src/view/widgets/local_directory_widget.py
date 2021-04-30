from src.view.widgets.directory_widget import DirectoryWidget
from src.model.widgets.local_directory import LocalDirectory


class LocalDirectoryWidget(DirectoryWidget):

    def __init__(self, dir: LocalDirectory, parent=None):
        super(LocalDirectoryWidget, self).__init__()
        self.parent = parent
        self.path = dir.get_path()
        self.name = dir.get_name()
        self.setText(self.name)
        if self.parent is not None:
            self.Sg_double_clicked.connect(self.parent.Sl_update_files_with_new_path)

    def double_clicked_action(self):
        self.Sg_double_clicked.emit(self.path)
