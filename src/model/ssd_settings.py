import os
import json
import math

path = None
config_path = os.path.dirname(os.path.realpath(__file__)) + "/settings.mer"

settings_list = ['path', 'quota']
n_settings = len(settings_list)


# TODO: check if json is in fact a json


def getpath():
    """
    Method used to get the application current root path (the one the user selected)

    :return: the current root path
    """
    return path


# returns false if quota is not set, otherwise raise FileNotFoundError if
# it cannot find the settings.mer and if all goes well it returns the
# quota

def getquota(default_value=True) -> str:
    value = getsetting('quota', default_value)
    if default_value:
        return int(value)
    else:
        return value


def getsetting(requested_setting: str, default_value=True) -> str:
    """
    getsetting is used to get requested setting from the setting file, the method can raise an
    exception if the setting file
    cannot be read or if the requested setting is not found (file corrupted or wrong setting)

    :param default_value: True means no converts will be done to the returned value I.E returned as read,
    False means it will be converted, atm works only with quota
    :param requested_setting: the setting to search for in the setting file, if the setting does not exists
    it raises an exception
    :return: False if the value is found but is not set I.E None
    """
    if path is None:
        raise FileNotFoundError(
            "path is set to None, cannot search for settings file")
    else:
        if is_path_valid(config_path):
            with open(config_path, "r") as file:
                data = json.load(file)
                for obj in data['settings']:
                    sett = obj[requested_setting]
                if sett == "None":
                    return False
                else:
                    if default_value:
                        return sett
                    else:
                        return convert_size(sett)
        else:
            raise FileNotFoundError(
                "Cannot find files in the following path" + config_path)


def setquota(quota: int) -> bool:
    """
    Method that writes on setting file the new quota value, can raise a FileNotFoundError or json error

    :param quota: the new disk quota in byte
    :return: True if the new value has been stored, False if not
    """
    int(quota)  # can raise ValueError
    if config_path is None:
        raise FileNotFoundError(
            "config path is not set, cannot search for setting file")
    else:
        print()
        if is_path_valid(config_path):
            with open(config_path, "r") as file:
                data = json.load(file)
                with open(config_path, "w") as output:
                    for obj in data['settings']:
                        obj['quota'] = quota
                    json.dump(data, output)
                    return True

        else:
            raise FileNotFoundError(
                "config path is set but setting file cannot be found or opened")

    return False


def setpath(new_path: str):
    """
    Set the new path

    :param new_path: the new path to save
    :return: Nothing
    """
    global path
    path = new_path


def write_new_settings_file(data: iter):
    """
    Method that write a new settings file, called when there is no setting file and a new one needs to be written.
    can raise ValueError if the vector is not ok or IOError with the file

    :param data: a vector containing all the settings value, they need to be in the same order as settings_list,The first value (data[0]) needs to be the path of the new setting file, this (data[0]) will not be stored on the file. the vector needs to be same or > length of the settings_list length
    :return: Nothing
    """
    # data in 0 is the full path for the setting file
    try:
        iter(data)
        if isinstance(data, str):
            raise ValueError(
                "Wrong argument, passed a string when needed a list/vector of data")
        elif len(data < n_settings):
            raise ValueError(
                "Passed a vector with less than " + n_settings + "values")
    except TypeError:
        error_string = "Wrong argument, passed" + \
            type(data) + \
            "when needed a list/vector of data"
        return ValueError(error_string)
    else:
        with open(data[0], "w") as outfile:
            print("Ho aperto il nuovo file e ci scrivo dentro")
            data.pop(0)  # rimuovo il path al file, non mi serve più
            jsonfile = {'settings': []}
            diz = create_settings_dict()
            jsonfile['settings'].append(diz)
            json.dump(jsonfile, outfile)


def is_path_valid(path_to_validate: str, extra_to_attach: str = "") -> bool:
    """
    Method used to check if the path is valid (I.E the path is a valid string and the file pointing at that
    path can be read

    :param path_to_validate: str with the path
    :param extra_to_attach: str to attach at the path, this is used to avoid doing None + Any as adding None to something will throw an exception
    :return: False if the path is not valid (None) or cannot be read
    """
    if path_to_validate is not None:
        try:
            with open(path_to_validate + extra_to_attach, "r"):
                return True
        except OSError:
            print("Errore lettura file")
            return False
    else:
        print("Path = none")
        return False


# controlla se termina con "/" altrimenti lo aggiunge


def setup_path(path_to_fix: str) -> str:
    """
    Method used to setup a correct directory pathing I.E adding / at the end of the path if it's missing.
    It can raise an exception if the param is not a string

    :param path_to_fix: str with path to check if it needs to be fixed
    :return: str with fixed path
    """
    if not isinstance(path_to_fix, str):
        raise TypeError(
            "Argument path_to_fix is not a string")
    else:
        # se non termina con "/" lo aggiungo
        if not path_to_fix.endswith("/"):
            return path_to_fix + "/"
        else:
            # altrimenti lascialo così
            return path_to_fix


def get_all_settings_values():
    """
    Method used to get all the setting values contained inside the setting file. Usually used when settings file
    need to change path

    :return: list with all the setting values, it will be padded with None value if needed
    """
    settings_value = []
    with open(path, "r") as json_file:
        data = json.load(json_file)

        # prende gli elementi innestati dentro a settings
        for obj in data['settings']:
            # add the elements inside our vector
            settings_value.append(obj)
        # while diff length between two vector add "None" to get vector
        # (padding the vector)
        while len(settings_value) < len(settings_list):
            settings_value.append("None")
        return settings_value


def create_settings_dict():
    """
    Method that creates a dictionary containing all the settings with their value ex {key1:2, key2:5}

    :return: the dictionary created
    """
    try:
        settings_value = get_all_settings_values()
    except IOError:
        settings_value = ['None'] * n_settings
    return dict(zip(settings_list, zip(settings_value)))


def convert_size(size_bytes):
    """
    Method used to convert from byte to the biggest representation

    :param size_bytes:
    :return: a string with the number and the new numeric base
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def getsettingspath():
    """
    Method used to get the settings file directory path

    :return: settings file directory path
    """
    return os.path.dirname(os.path.realpath(__file__))
