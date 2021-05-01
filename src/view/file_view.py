from PySide6.QtCore import (QSettings, QUrl, Slot, Qt, Signal)
from PySide6.QtGui import (QDesktopServices)
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QScrollArea, QLabel, QMenu)

from src.model.file_model import FileModel
from src.view.layouts.flowlayout import FlowLayout
from src.view.widgets.local_directory_widget import LocalDirectoryWidget
from src.view.widgets.local_file_widget import LocalFileWidget


class FileView(QWidget):
    Sg_update_files_with_new_path = Signal(str)
    Sg_show_path = Signal()

    def __init__(self, model: FileModel, parent=None):
        super(FileView, self).__init__(parent)

        self.env_settings = QSettings()
        self._model = model

        self.title = QLabel("File sincronizzati", self)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setAccessibleName("Title")

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setAccessibleName("FileScroll")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        # contenitore per file
        self.fileWindow = QWidget(self)
        self.fileLayout = FlowLayout()
        self.fileLayout.setContentsMargins(0, 0, 0, 0)

        self.fileWindow.setParent(self.scrollArea)
        self.fileWindow.setLayout(self.fileLayout)

        self.scrollArea.setWidget(self.fileWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.Sl_model_changed()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        file_manager_action = context_menu.addAction("Apri file manager")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == file_manager_action:
            self.Sg_show_path.emit()

    @Slot()
    def Sl_show_path_button_clicked(self) -> None:
        path = QUrl.fromUserInput(self.env_settings.value("sync_path"))
        QDesktopServices.openUrl(path)

    @Slot()
    def Sl_model_changed(self) -> None:
        list_of_files, list_of_dirs = self._model.get_data()

        for i in reversed(range(self.fileLayout.count())):
            self.fileLayout.itemAt(i).widget().setParent(None)
        for i in list_of_dirs:
            self.fileLayout.addWidget(LocalDirectoryWidget(i, self))
        for i in list_of_files:
            self.fileLayout.addWidget(LocalFileWidget(i))

    @Slot(str)
    def Sl_update_files_with_new_path(self, path: str) -> None:
        self.Sg_update_files_with_new_path.emit(path)
