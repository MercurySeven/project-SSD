from PySide6.QtCore import (Qt, Signal, Slot)
from PySide6.QtGui import (QIntValidator)
from PySide6.QtWidgets import (QWidget, QProgressBar, QLabel,
                               QVBoxLayout, QLineEdit, QComboBox, QPushButton)
import bitmath

from src.model.settings_model import SettingsModel


class SetQuotaDiskWidget(QWidget):

    Sg_view_changed = Signal()

    def __init__(self, model: SettingsModel, parent=None):
        super(SetQuotaDiskWidget, self).__init__(parent)

        self._model = model

        self.setAccessibleName("InfoBox")

        self.title = QLabel()
        self.title.setText("Quota disco")
        self.title.setAccessibleName("Subtitle")

        # Barra riempimento disco
        self.progress_label = QLabel()
        self.progress_label.setText("Spazio occupato")
        self.progress_label.setAccessibleName("Subtitle")

        self.disk_progress = QProgressBar()
        self.disk_progress.setFormat("")

        self.disk_quota = QLabel()

        # Modifica spazio dedicato
        self.spaceLabel = QLabel("Spazio dedicato")
        self.spaceLabel.setAccessibleName("Subtitle")

        self.dedicated_space = QLineEdit()
        self.dedicated_space.setValidator(QIntValidator())

        self.sizes_box = QComboBox()
        _path_size = model.convert_size(model.get_size())
        _disk_free = model.convert_size(model.get_free_disk())
        print(_path_size)
        print(_disk_free)
        gb_in_byte = bitmath.parse_string(_disk_free).to_Byte()
        print(gb_in_byte)

        self.populate_size_box(_path_size[-3:], _disk_free[-3:])

        self.change_quota_button = QPushButton("Cambia quota disco")

        self.change_quota_button.clicked.connect(self.Sl_dedicated_space_changed)

        # layout
        disk_layout = QVBoxLayout()
        disk_layout.setAlignment(Qt.AlignLeft)
        disk_layout.addWidget(self.progress_label)
        disk_layout.addWidget(self.disk_progress)
        disk_layout.addWidget(self.disk_quota)
        disk_layout.addWidget(self.spaceLabel)
        disk_layout.addWidget(self.dedicated_space)
        disk_layout.addWidget(self.sizes_box)
        disk_layout.addWidget(self.change_quota_button)

        self.setLayout(disk_layout)
        self.Sl_model_changed()

    @Slot()
    def Sl_dedicated_space_changed(self):
        self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        new_max_quota = self._model.get_quota_disco()
        folder_size_parsed = bitmath.parse_string(self._model.convert_size(self._model.get_size()))
        self.disk_quota.setText(f"{folder_size_parsed} su {new_max_quota}")
        max_size_parsed = bitmath.parse_string(new_max_quota)
        self.dedicated_space.setText(str(max_size_parsed.value))
        self.sizes_box.setCurrentText(max_size_parsed.unit)
        # Prendo dimensione corrente della sync folder e della quota disco
        # e metto in proporzione con quotadisco:100=syncfolder:x
        _progress_bar_max_value = 100
        _tmp = folder_size_parsed.to_Byte().value*_progress_bar_max_value
        _progress_bar_current_percentage = _tmp/max_size_parsed.to_Byte().value

        # Inserisco nuovi valori nella progress bar
        self.disk_progress.setRange(0, _progress_bar_max_value)
        self.disk_progress.setValue(_progress_bar_current_percentage)

    def populate_size_box(self, _min, _max, ) -> None:
        """
        This method populates the size box with only the available units
        ex hdd has only <1gb so gb will not be used, the current folder is
        heavier than 1mb so kb will not be used.
        :param _min: minimum value
        :param _max: maximum value
        :return: None
        """
        _sizes = "B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"
        lower_bound = _sizes[_sizes.index(_min):]
        upper_bound = lower_bound[:lower_bound.index(_max)+1]
        self.sizes_box.addItems(upper_bound)
