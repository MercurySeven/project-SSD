from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog)
from PySide6.QtCore import (Slot, Signal)
from src.model.settings_model import SettingsModel


class SetPathView(QWidget):
    Sg_view_changed = Signal(str)

    def __init__(self, model: SettingsModel, parent=None):
        super(SetPathView, self).__init__(parent)

        self._model = model
        self.debug = False
        self.titolo = QLabel()
        self.titolo.setText("Cartella da sincronizzare")
        self.titolo.setAccessibleName("Subtitle")

        self.path = QLabel()
        self.path.setText(self._model.get_path())

        self.change_path_button = QPushButton("Cambia")
        self.change_path_button.setMaximumWidth(150)

        layout = QVBoxLayout()
        layout.addWidget(self.titolo)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.path)
        sub_layout.addWidget(self.change_path_button)

        layout.addLayout(sub_layout)
        self.setLayout(layout)

        self.change_path_button.clicked.connect(self.Sl_show_file_dialog)

    @Slot()
    def Sl_model_changed(self):
        self.path.setText(self._model.get_path())

    @Slot()
    def Sl_show_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        if dialog.exec_():
            # Serve per fare in modo che il test abbia una stringa da usare
            sync_path = ["test"] if self.debug else dialog.selectedFiles()
            if len(sync_path) == 1:
                self.Sg_view_changed.emit(sync_path[0])
