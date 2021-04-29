import bitmath
from PySide6.QtCore import (Qt, Signal, Slot)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (QWidget, QProgressBar, QLabel,
                               QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton)

from src.model.settings_model import SettingsModel


class SetQuotaDiskWidget(QWidget):
    Sg_view_changed = Signal()

    def __init__(self, model: SettingsModel, parent=None):
        super(SetQuotaDiskWidget, self).__init__(parent)

        self._model = model

        self.setAccessibleName("InfoBox")

        self.title = QLabel()
        self.title.setText("Spazio di archiviazione")
        self.title.setAccessibleName("Title2")

        self.sottotitolo = QLabel()
        self.sottotitolo.setAccessibleName('Sottotitolo')
        self.sottotitolo.setText(
            "Cambia lo spazio di archiviazione destinato alla cartella sincronizzata")

        # Barra riempimento disco
        self.progress_label = QLabel()
        self.progress_label.setText("Spazio occupato:")

        self.disk_progress = QProgressBar()
        self.disk_progress.setFormat("")

        self.disk_quota = QLabel()

        # Modifica spazio dedicato
        self.spaceLabel = QLabel(" ")

        self.dedicated_space = QLineEdit()
        self.dedicated_space.setValidator(QDoubleValidator())

        self.sizes_box = QComboBox()
        self.sizes_box.wheelEvent = lambda event: None
        _path_size = bitmath.parse_string(model.convert_size(model.get_size()))
        _disk_free = bitmath.parse_string(model.convert_size(model.get_free_disk()))

        self.populate_size_box(_path_size, _disk_free)

        self.change_quota_button = QPushButton("Cambia quota disco")
        self.change_quota_button.setMaximumWidth(150)

        self.change_quota_button.clicked.connect(self.Sl_dedicated_space_changed)
        self.dedicated_space.returnPressed.connect(self.Sl_dedicated_space_changed)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.spaceLabel)
        self.buttonLayout.addWidget(self.change_quota_button)
        self.buttonLayout.addWidget(self.spaceLabel)

        set_space_layout = QHBoxLayout()
        set_space_layout.addWidget(self.dedicated_space)
        set_space_layout.addWidget(self.sizes_box)

        quota_layout = QHBoxLayout()
        quota_layout.setAlignment(Qt.AlignLeft)
        quota_layout.addWidget(self.progress_label)
        quota_layout.addWidget(self.disk_quota)

        # layout
        disk_layout = QVBoxLayout()
        disk_layout.setAlignment(Qt.AlignLeft)
        disk_layout.addWidget(self.title)
        disk_layout.addWidget(self.sottotitolo)
        disk_layout.addWidget(self.spaceLabel)
        disk_layout.addLayout(quota_layout)
        disk_layout.addWidget(self.disk_progress)
        disk_layout.addWidget(self.spaceLabel)
        disk_layout.addLayout(set_space_layout)
        disk_layout.addLayout(self.buttonLayout)

        self.setLayout(disk_layout)
        self.Sl_model_changed()

    @Slot()
    def Sl_dedicated_space_changed(self):
        self.Sg_view_changed.emit()

    @Slot()
    def Sl_model_changed(self):
        new_max_quota = self._model.get_quota_disco()
        _quota = self._model.get_quota_disco_raw()
        _folder_size = self._model.get_size()

        folder_size_parsed = bitmath.parse_string(self._model.convert_size(_folder_size))
        quota_parsed = bitmath.parse_string(self._model.convert_size(_quota))

        self.disk_quota.setText(f"{folder_size_parsed} su {new_max_quota} in uso")
        max_size_parsed = bitmath.parse_string(new_max_quota)
        self.dedicated_space.setText(str(max_size_parsed.value))
        self.sizes_box.setCurrentText(max_size_parsed.unit)
        free_disk_parsed = bitmath.parse_string(
            self._model.convert_size(self._model.get_free_disk()))
        self.populate_size_box(folder_size_parsed, free_disk_parsed)

        # Prendo dimensione corrente della sync folder e della quota disco
        # e metto in proporzione con quotadisco:100=syncfolder:x
        _progress_bar_max_value = 100
        _tmp = folder_size_parsed.to_Byte().value * _progress_bar_max_value
        _progress_bar_current_percentage = _tmp / max_size_parsed.to_Byte().value

        # Inserisco nuovi valori nella progress bar
        self.disk_progress.setRange(0, _progress_bar_max_value)
        self.disk_progress.setValue(_progress_bar_current_percentage)

        # Se la cartella occupa più spazio di quanto voluto allora la porto a quanto occupa
        if quota_parsed < folder_size_parsed:
            self.dedicated_space.setText(str(folder_size_parsed.value))
            self.sizes_box.setCurrentText(folder_size_parsed.unit)
            self.Sg_view_changed.emit()

    def populate_size_box(self, _min: str, _max: str, ) -> None:
        """
        This method populates the size box with only the available units
        ex hdd has only <1gb so gb will not be used, the current folder is
        heavier than 1mb so kb will not be used.
        :param _min: minimum value with unit ex 10 KiB or just 'KiB'
        :param _max: maximum value with unit ex 10 KiB or just 'KiB'
        :return: None
        """
        _sizes = "Byte", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"
        # Converto in ogni caso a string, in caso in cui venga passato un oggetto
        # tipo bitmath

        _min = str(_min)
        _max = str(_max)

        # Rimuovo eventuali numeri e caratteri extra, tengo solo l'unità di misura
        _min = ''.join(i for i in _min if not i.isdigit() and i != '.')
        _max = ''.join(i for i in _max if not i.isdigit() and i != '.')

        # Rimuovo possibili spazi ad inizio e fine stringa
        _min = _min.strip()
        _max = _max.strip()

        # Rimuovo dal vettore di possibili unità di misura tutte le unità sotto il lower bound
        lower_bound = _sizes[_sizes.index(_min):]
        # Rimuovo dal vettore di possibili unità di misura tutte le unità sopra l'upper bound
        upper_bound = lower_bound[:lower_bound.index(_max) + 1]

        # Pulisco il vecchio combo box
        self.sizes_box.clear()

        # Inserisco nuovi valori
        self.sizes_box.addItems(upper_bound)
