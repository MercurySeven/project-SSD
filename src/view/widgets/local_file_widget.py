from PySide6.QtCore import (Slot, QUrl)
from PySide6.QtGui import (QDesktopServices)

from src.model.widgets.local_file import LocalFile
from src.view.widgets.file_widget import FileWidget


class LocalFileWidget(FileWidget):

    def __init__(self, file: LocalFile):
        super(LocalFileWidget, self).__init__(file)

        self.size = file.get_size()
        self.path = file.get_path()

        tooltip = (f"Nome: {self.name}\n"
                   f"Ultima modifica: {self.last_modified_date}\n"
                   f"Dimensioni: {self.size}")

        self.setToolTip(tooltip)

    @Slot()
    def Sl_on_double_click(self):
        file_path = QUrl.fromUserInput(self.path)
        QDesktopServices.openUrl(file_path)
