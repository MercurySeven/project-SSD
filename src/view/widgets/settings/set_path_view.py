from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog)
from PySide6.QtCore import (Slot, Signal)
from model.widgets.settings import SetPathModel
from controllers.widgets.settings import SetPathController


class SetPathView(QWidget):

    Sg_new_path = Signal(str)

    def __init__(self,
                 model: SetPathModel,
                 controller: SetPathController,
                 parent=None):
        super(SetPathView, self).__init__(parent)

        self.model = model
        self.controller = controller

        self.titolo = QLabel()
        self.titolo.setText("Cartella da sincronizzare")
        self.titolo.setAccessibleName("Subtitle")

        self.path = QLabel()
        self.path.setText(self.model.get_path())

        self.change_path_button = QPushButton("Cambia")
        self.change_path_button.setMaximumWidth(150)

        layout = QVBoxLayout()
        layout.addWidget(self.titolo)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.path)
        sub_layout.addWidget(self.change_path_button)

        layout.addLayout(sub_layout)
        self.setLayout(layout)

        self.change_path_button.clicked.connect(
            lambda: self.Sl_show_file_dialog())
        self.Sg_new_path.connect(self.controller.Sl_show_file_dialog_result)
        self.model.Sg_model_changed.connect(lambda: self.Sl_model_changed())

    @Slot()
    def Sl_model_changed(self):
        self.path.setText(self.model.get_path())

    @Slot()
    def Sl_show_file_dialog(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        if dialog.exec_():
            sync_path = dialog.selectedFiles()
            if len(sync_path) == 1:
                self.Sg_new_path.emit(sync_path[0])
