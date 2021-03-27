import configparser
import os.path
import logging
from typing import Optional

file_name = "config.ini"


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
        "policy": "1",
        "is_sync": "off"
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
        logger.info("File di impostazioni non esistente, verrà creato")
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
        logger.warning("Il valore di quota disco non e' int")
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
        logger.warning("Il valore di policy non e' int")
        update_policy(1)
        return 1


def get_is_synch() -> bool:
    "Ritorna lo stato di sincronizzazione"
    return get_config("General", "is_sync") == "on"


def update_config(section: str, passed_config: str, value: str) -> None:
    """Aggiunge o aggiorna una config"""
    if section not in config.sections():
        config[section] = {}

    config[section][passed_config] = value
    __write_on_file()
    logger.info(f"New save: {section}/{passed_config} with value: {value}")


def update_quota_disco(value: str) -> None:
    """Aggiorna la quota disco"""
    update_config("General", "quota", value)


def update_policy(policy: int) -> None:
    """Aggiorna la policy"""
    update_config("General", "policy", str(policy))


def update_is_sync(state: bool) -> None:
    """Aggiorna lo stato di sincronizzazione"""
    update_config("General", "is_sync", "on" if state else "off")


def update_username(username: str) -> None:
    """ Aggiorna l'username salvato """
    update_config("Login", "username", username)


def update_password(password: str) -> None:
    """ Aggiorna la password salvata """
    update_config("Login", "password", password)


def update_login_credentials(username: str, password: str) -> None:
    update_config("Login", "username", username)
    update_config("Login", "password", password)


config = configparser.ConfigParser()
logger = logging.getLogger("settings")
if os.path.exists(file_name):
    last_update = os.path.getmtime(file_name)

check_file()
