from PySide6.QtCore import (Slot)
from src.model.widgets.remote_file import RemoteFile
from src.view.widgets.file_widget import FileWidget


class RemoteFileWidget(FileWidget):

    def __init__(self, file: RemoteFile):
        super(RemoteFileWidget, self).__init__(file)

        self.status = file.get_status()
        self.size = file.get_size()
        self.last_editor = file.get_last_editor()

        tooltip = (f"Nome: {self.name}\n"
                   f"Ultima modifica: {self.last_modified_date}\n"
                   f"Dimensioni: {self.size}\n"
                   f"Ultimo editor: {self.last_editor}")

        self.setToolTip(tooltip)

    @Slot()
    def Sl_on_double_click(self):
        pass
