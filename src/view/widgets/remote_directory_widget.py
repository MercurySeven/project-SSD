from src.view.widgets.directory_widget import DirectoryWidget
from src.model.widgets.remote_directory import RemoteDirectory
from PySide6.QtCore import Slot


class RemoteDirectoryWidget(DirectoryWidget):

    def __init__(self, dir: RemoteDirectory, parent=None):
        super(RemoteDirectoryWidget, self).__init__(dir, parent)
        self.id = dir._node.get_payload().id

        if self.parent is not None:
            self.Sg_double_clicked.connect(self.parent.Sl_update_files_with_new_path)

    @Slot()
    def Sl_check_double_click(self):
        success = False
        if self.timer.isActive():
            time = self.timer.remainingTime()
            if time > 0:
                self.Sg_double_clicked.emit(self.id)
                success = True
                self.timer.stop()
            if time <= 0:
                self.timer.start(250)

        if self.timer.isActive() is False and success is False:
            self.timer.start(250)
