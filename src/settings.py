import configparser
import os.path
import math
import logging

from PySide6.QtCore import QSettings


class Settings:

    def __init__(self):
        self.filename = "config.ini"
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger("settings")
        self.__check_file()
        self.settings = QSettings()

    def __check_file(self):
        if os.path.isfile(self.filename):
            self.logger.info("Carico impostazioni da file: " + self.filename)
            self.__read_from_file()
        else:
            self.logger.info(
                "File di impostazioni non esistente, verrà creato")
            self.create_standard_settings()

    def create_standard_settings(self) -> None:
        """Genera il file di impostazioni standard"""
        self.config["General"] = {
            "Quota": "1024"
        }

        self.config["Connection"] = {
            "address": "http://20.56.176.12",
            "port": "80"
        }

        self.__write_on_file()

    def __read_from_file(self) -> None:
        """Legge le impostazioni dal file"""
        self.config.read(self.filename)
        self.last_update = os.path.getmtime(self.filename)

    def __write_on_file(self) -> None:
        """Salva le impostazioni su file"""
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
        self.last_update = os.path.getmtime(self.filename)

    def get_sections(self) -> list:
        """Restituisce le sezioni del file"""
        return self.config.sections()

    def get_config(self, section: str, config: str) -> str:
        """Ritorna il valore della config desiderata, None se inesistente"""
        new_time = os.path.getmtime(self.filename)

        # Il file è stato modificato lo ricarico
        if new_time > self.last_update:
            self.__read_from_file()
            self.logger.debug("Impostazioni cambiate, file ricaricato")

        if section not in self.get_sections():
            return None
        if config not in self.config[section]:
            return None
        return self.config[section][config]

    def get_server_url(self) -> str:
        """Resituisce l'indirizzo del server"""
        address = self.get_config("Connection", "address")
        port = self.get_config("Connection", "port")

        # Elimino lo slash se presente
        if address[-1] == "/":
            address = address[:-1]

        return address + ":" + port + "/"

    def get_quota_disco(self, default_value=True) -> str:
        """Restituisce la quota disco"""
        try:
            value = self.get_config("General", "quota")
            int(value)  # test per controllare se è int
            if default_value:
                return value
            else:
                return self.convert_size(value)
        except ValueError:
            self.logger.warning("Il valore di quota disco non è int")
            self.update_config("General", "quota", "1024")
            return "1024"

    def update_config(self, section: str, config: str, value: str) -> None:
        """Aggiunge o aggiorna una config"""
        self.config[section][config] = value
        self.__write_on_file()
        self.logger.info("New save: " + section + "/" +
                         config + " with value: " + value)

    def update_quota_disco(self, value: str) -> None:
        """Aggiorna la quota disco"""
        self.update_config("General", "quota", value)

    @staticmethod
    def convert_size(size_bytes: str) -> str:
        """
        Method used to convert from byte to the biggest representation

        :param size_bytes:
        :return: a string with the number and the new numeric base
        """
        # TODO: Forse è da spostare, dato che non c'entra molto con settings
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def get_path(self) -> str:
        return self.settings.value("sync_path")

    def update_path(self, new_path: str) -> None:
        self.settings.setValue("sync_path", new_path)
        self.settings.sync()  # Aggisce come da cache e forza l'aggioramento
