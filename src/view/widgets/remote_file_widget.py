from PySide6.QtCore import (Slot)
from src.model.widgets.remote_file import RemoteFile
from src.view.widgets.file_widget import FileWidget


class RemoteFileWidget(FileWidget):

    def __init__(self, file: RemoteFile):
        super(RemoteFileWidget, self).__init__(file)

        self.status = file.get_status()

        self.setText(self.name)
        self.setToolTip(f"Nome: {self.name}\nUltima modifica: {self.last_modified_date}")

    @Slot()
    def Sl_on_double_click(self):
        pass
