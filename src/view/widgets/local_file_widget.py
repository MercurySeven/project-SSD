import os

from PySide6.QtCore import (QPoint, QSize, Slot, QUrl, Qt)
from PySide6.QtGui import (QDesktopServices, QIcon, QPainter, QPixmap)

from src import assets_path
from src.model.widgets.local_file import LocalFile
from src.view.widgets.file_widget import FileWidget
from src.view.stylesheets.qssManager import resource_path


class LocalFileWidget(FileWidget):

    def __init__(self, file: LocalFile):
        super(LocalFileWidget, self).__init__(file)

        self.size = file.get_size()
        self.path = file.get_path()

        tooltip = (f"Nome: {self.name}\n"
                   f"Ultima modifica: {self.last_modified_date}\n"
                   f"Dimensioni: {self.size}")

        self.show_synced(False)
        self.setToolTip(tooltip)

    @Slot()
    def Sl_on_double_click(self):
        file_path = QUrl.fromUserInput(self.path)
        QDesktopServices.openUrl(file_path)

    def toggle(self) -> None:
        self.is_sync = not self.is_sync
        self.show_synced()

    def get_icon(self, is_sync: bool) -> QPixmap:
        if is_sync:
            return QPixmap(resource_path(
                os.path.join(assets_path.ASSETS_PATH, 'icons/Transfer.png')))
        return QPixmap(resource_path(
            os.path.join(assets_path.ASSETS_PATH, 'icons/Check.png')))

    def show_synced(self, is_sync: bool) -> None:
        p1 = QPixmap(self.icon().pixmap(self.icon().actualSize(QSize(1024, 1024))))
        p2 = self.get_icon(is_sync)

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
