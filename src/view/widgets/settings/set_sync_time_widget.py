import re

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QComboBox, QLabel, QWidget, QVBoxLayout

from src.model.settings_model import SettingsModel


class SetSyncTimeWidget(QWidget):
    Sg_view_changed = Signal()

    def __init__(self, model: SettingsModel, parent=None):
        super(SetSyncTimeWidget, self).__init__(parent)

        self._time_list = ["5s", "10s", "15s", "15m", "30m", "45m"]
        self._time_in_sec = []
        for curr_time in self._time_list:
            time_int = int(re.search(r'\d+', curr_time).group())
            if 'm' in curr_time:
                time_int = time_int * 60
            if 'h' in curr_time:
                time_int = time_int * 3600
            self._time_in_sec.append(time_int)

        self._model = model

        self._titolo = QLabel()
        self._titolo.setText("Seleziona finestra temporale per la sincronizzazione")
        self._titolo.setAccessibleName('Subtitle')

        self.time_box = QComboBox()
        self.time_box.addItems(self._time_list)
        self.Sl_model_changed()

        layout = QVBoxLayout()
        layout.addWidget(self._titolo)
        layout.addWidget(self.time_box)

        self.setLayout(layout)

        # connect signal
        self.time_box.currentIndexChanged.connect(self.Sl_time_checked)

    @Slot()
    def Sl_time_checked(self):
        self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        time = self._model.get_sync_time()
        i: int = 0
        for el in self._time_in_sec:
            if time == el:
                self.time_box.setCurrentIndex(i)
            i += 1
