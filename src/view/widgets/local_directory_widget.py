from src.view.widgets.directory_widget import DirectoryWidget
from src.model.widgets.local_directory import LocalDirectory
from PySide6.QtCore import Slot


class LocalDirectoryWidget(DirectoryWidget):

    def __init__(self, dir: LocalDirectory, parent=None):
        super(LocalDirectoryWidget, self).__init__(dir, parent)
        self.path = dir.get_path()

        if self.parent is not None:
            self.Sg_double_clicked.connect(self.parent.Sl_update_files_with_new_path)

    @Slot()
    def Sl_check_double_click(self):
        success = False
        if self.timer.isActive():
            time = self.timer.remainingTime()
            if time > 0:
                self.Sg_double_clicked.emit(self.path)
                success = True
                self.timer.stop()
            if time <= 0:
                self.timer.start(250)

        if self.timer.isActive() is False and success is False:
            self.timer.start(250)
