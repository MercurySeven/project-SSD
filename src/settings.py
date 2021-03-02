import configparser
import os.path
import logging
from typing import Optional

file_name = "config.ini"
config = configparser.ConfigParser()
logger = logging.getLogger("settings")
last_update = os.path.getmtime(file_name)
# check_file()


def check_file() -> None:
    print(os.path.abspath(file_name))
    if os.path.isfile(file_name):
        logger.info("Carico impostazioni da file: " + file_name)
        __read_from_file()
    else:
        logger.info(
            "File di impostazioni non esistente, verrà creato")
        create_standard_settings()


def create_standard_settings() -> None:
    """Genera il file di impostazioni standard"""
    config["General"] = {
        "Quota": "1024"
    }

    config["Connection"] = {
        "address": "http://20.56.176.12",
        "port": "80"
    }

    __write_on_file()


def __read_from_file() -> None:
    """Legge le impostazioni dal file"""
    config.read(file_name)
    global last_update
    last_update = os.path.getmtime(file_name)


def __write_on_file() -> None:
    """Salva le impostazioni su file"""
    with open(file_name, 'w') as configfile:
        config.write(configfile)
    global last_update
    last_update = os.path.getmtime(file_name)


def get_config(section: str, passed_config: str) -> Optional[str]:
    """Ritorna il valore della config desiderata, None se inesistente"""
    new_time = os.path.getmtime(file_name)

    # Il file è stato modificato lo ricarico
    if new_time > last_update:
        __read_from_file()
        logger.debug("Impostazioni cambiate, file ricaricato")

    if section not in config.sections():
        return None
    if passed_config not in config[section]:
        return None
    return config[section][passed_config]


def get_server_url() -> str:
    """Resituisce l'indirizzo del server"""
    address = get_config("Connection", "address")
    port = get_config("Connection", "port")

    # Elimino lo slash se presente
    if address[-1] == "/":
        address = address[:-1]

    return address + ":" + port + "/"


def get_quota_disco() -> int:
    """Restituisce la quota disco"""
    try:
        value = get_config("General", "quota")
        result = int(value)
        return result
    except ValueError:
        logger.warning("Il valore di quota disco non è int")
        update_config("General", "quota", "1024")
        return 1024


def update_config(section: str, passed_config: str, value: str) -> None:
    """Aggiunge o aggiorna una config"""
    if section not in config.sections():
        config[section] = {}

    config[section][passed_config] = value
    __write_on_file()
    logger.info("New save: " + section + "/" +
                passed_config + " with value: " + value)


def update_quota_disco(value: str) -> None:
    """Aggiorna la quota disco"""
    update_config("General", "quota", value)
