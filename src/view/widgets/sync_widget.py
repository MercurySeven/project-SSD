from PySide6.QtCore import (Signal, Slot, Qt, QSize)
from PySide6.QtWidgets import (QPushButton, QLabel, QVBoxLayout, QWidget)
from PySide6.QtGui import (QIcon)

from src.model.widgets.sync_model import SyncModel


class SyncWidget(QWidget):

    Sg_view_changed = Signal()

    def __init__(self, model: SyncModel, parent=None):
        super(SyncWidget, self).__init__(parent)

        self._model = model

        self.watch_label = QLabel(self)
        self.watch_label.setAlignment(Qt.AlignCenter)
        self.watch_label.setText("SYNC")
        self.watch_label.setAccessibleName("Title")

        self.running_label = QLabel(self)
        self.running_label.setAlignment(Qt.AlignCenter)
        self.running_label.setText("Disattivata")
        self.running_label.setAccessibleName("Subtitle")

        self.sync_button = QPushButton(self)
        self.sync_button.setIcon(QIcon('./icons/reload.png'))
        self.sync_button.setIconSize(QSize(50, 50))
        self.sync_button.setCheckable(True)
        self.sync_button.setAccessibleName('HighlightButton')

        self.menu_label = QLabel(self)
        self.menu_label.setAlignment(Qt.AlignCenter)
        self.menu_label.setText("• • •")

        # create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.watch_label)
        self.layout.addWidget(self.running_label)
        self.layout.addWidget(self.sync_button)
        self.layout.addWidget(self.menu_label)
        self.setLayout(self.layout)

        self.sync_button.clicked.connect(self.Sl_button_clicked)
        self.Sl_model_changed()

    @Slot()
    def Sl_button_clicked(self):
        self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        self.sync_button.setChecked(self._model.get_state())
        if self._model.get_state():
            self.running_label.setText("Attivata")
        else:
            self.running_label.setText("Disattivata")
