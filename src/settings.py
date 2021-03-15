import configparser
import os.path
import logging
from typing import Optional


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


def create_standard_settings() -> None:
    """Genera il file di impostazioni standard"""
    config["General"] = {
        "quota": "1024",
        "policy": "1"
    }

    # TODO: Da rimuovere
    config["Login"] = {
        "username": "user",
        "password": "pwd"
    }

    __write_on_file()


def check_file() -> None:
    if os.path.isfile(file_name):
        logger.info("Carico impostazioni da file: " + file_name)
        __read_from_file()
    else:
        logger.info(
            "File di impostazioni non esistente, verrà creato")
        create_standard_settings()


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


def get_quota_disco() -> int:
    """Restituisce la quota disco"""
    try:
        value = get_config("General", "quota")
        result = int(value)
        return result
    except ValueError:
        logger.warning("Il valore di quota disco non è int")
        update_quota_disco("1024")
        return 1024


def get_username() -> str:
    """Non usare questo metodo"""
    return get_config("Login", "username")


def get_password() -> str:
    """Non usare questo metodo"""
    return get_config("Login", "password")


def get_policy() -> int:
    "Ritorna la policy salvata"
    try:
        return int(get_config("General", "policy"))
    except ValueError:
        logger.warning("Il valore di policy è errata")
        update_policy(1)
        return 1


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


def update_policy(policy: int) -> None:
    """Aggiorna la policy"""
    update_config("General", "policy", str(policy))


# Assoulutamente da sistemare, fatto per evitare di testare
# direttamente sul file di config personale
file_name = "config.ini"
config = configparser.ConfigParser()
logger = logging.getLogger("settings")
if os.path.exists(file_name):
    last_update = os.path.getmtime(file_name)

check_file()
