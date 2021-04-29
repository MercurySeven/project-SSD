from PySide6.QtCore import (Qt, Signal, Slot)
from PySide6.QtGui import QDoubleValidator
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
        self.dedicated_space.setValidator(QDoubleValidator())

        self.sizes_box = QComboBox()
        _path_size = bitmath.parse_string(model.convert_size(model.get_size()))
        _disk_free = bitmath.parse_string(model.convert_size(model.get_free_disk()))

        self.populate_size_box(_path_size, _disk_free)

        self.change_quota_button = QPushButton("Cambia quota disco")

        self.change_quota_button.clicked.connect(self.Sl_dedicated_space_changed)
        self.dedicated_space.returnPressed.connect(self.Sl_dedicated_space_changed)

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
        """
        Slot collegato ai segnali del model, aggiorna la vista con i nuovi valori
        :return: None
        """

        # Prendo quota disco con unità e il peso della cartella senza unità (Byte default)
        new_max_quota = self._model.get_quota_disco()
        _folder_size = self._model.get_size()

        # Converto ad oggetto bitmath il peso della cartella e la quota disco
        folder_size_parsed = bitmath.parse_string(self._model.convert_size(_folder_size))
        quota_disco_parsed = bitmath.parse_string(new_max_quota)

        # Imposto la textbox che mi dice quanto peso ho occupato su quello disponibile
        self.disk_quota.setText(f"{folder_size_parsed} su {new_max_quota}")

        # Imposto la textbox che richiede input
        self.dedicated_space.setText(str(quota_disco_parsed.value))
        # Prendo quanto disco ho disponibile e la sua unità di misura
        free_disk_parsed = bitmath.parse_string(
            self._model.convert_size(self._model.get_free_disk()))

        self.populate_size_box(folder_size_parsed, free_disk_parsed)
        # Imposto l'unità di misura mostrata
        self.sizes_box.setCurrentText(quota_disco_parsed.unit)

        # Prendo dimensione corrente della sync folder e della quota disco
        # e metto in proporzione con quotadisco:100=syncfolder:x
        _progress_bar_max_value = 100
        _tmp = folder_size_parsed.to_Byte().value * _progress_bar_max_value
        _progress_bar_current_percentage = _tmp / quota_disco_parsed.to_Byte().value

        # Inserisco nuovi valori nella progress bar
        self.disk_progress.setRange(0, _progress_bar_max_value)
        self.disk_progress.setValue(_progress_bar_current_percentage)

        # Se la cartella occupa più spazio di quanto voluto allora la porto a quanto occupa
        if quota_disco_parsed < folder_size_parsed:
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
