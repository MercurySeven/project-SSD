import os
import json
import math

path = None
config_path = os.path.dirname(os.path.realpath(__file__)) + "/settings.mer"

settings_list = ['path', 'quota']
n_settings = len(settings_list)

# TODO: check if json is in fact a json


def getpath():
    return path

# returns false if quota is not set, otherwise raise FileNotFoundError if
# it cannot find the settings.mer and if all goes well it returns the
# quota


def getquota(byte_result= True):
    if path is None:
        raise FileNotFoundError(
            "path is set to None, cannot search for settings file")
    else:
        if is_path_valid(config_path):
            with open(config_path, "r") as file:
                data = json.load(file)
                if len(data['settings'][0]) >= n_settings:
                    for obj in data['settings']:
                        quota = obj['quota']
                    if quota == "None":
                        return False
                    else:
                        if byte_result:
                            return int(quota)
                        else:
                            return convert_size(quota)
                else:
                    return False
        else:
            raise FileNotFoundError(
                "Cannot find files in the following path" + config_path)


def setquota(quota: int) -> bool:
    int(quota)  # può lanciare ValueError
    if config_path is None:
        raise FileNotFoundError(
            "config path is not set, cannot search for setting file")
    else:
        print()
        if is_path_valid(config_path):
            with open(config_path, "r") as file:
                data = json.load(file)
                if len(data['settings'][0]) >= n_settings:
                    with open(config_path, "w") as output:
                        for obj in data['settings']:
                            obj['quota'] = quota
                        json.dump(data, output)
                        return True
                else:
                    raise EOFError(
                        "File is corrupted, it does "
                        "not contain at least" + n_settings + "lines")

        else:
            raise FileNotFoundError(
                "config path is set but setting file cannot be found or opened")

    return False


def setpath(new_path: str):
    global path
    path = new_path


def write_new_settings_file(data: iter):
    # data in 1 = x, 2 = y etc
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
        return ValueError(
            "Wrong argument, passed" + type(data) + "when needed a list/vector of data")
    else:
        with open(data[0], "w") as outfile:
            print("Ho aperto il nuovo file e ci scrivo dentro")
            data.pop(0)  # rimuovo il path al file, non mi serve più
            jsonfile = {'settings': []}
            diz = create_settings_dict()
            jsonfile['settings'].append(diz)
            json.dump(jsonfile, outfile)


def is_path_valid(path_to_validate: str, extra_to_attach: str = "") -> bool:
    # i use two arguments because if i have to do path + filename and path is
    # None raises an exception, now i can firstly check if path is None and
    # then add them
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
    if not isinstance(path_to_fix, str):
        raise TypeError(
            "Passato un oggetto che non è una stringa come path")
    else:
        if not path_to_fix.endswith("/"):
            return path_to_fix + "/"
        else:
            return path_to_fix


def get_all_settings_values():
    settings_value = []
    with open(path, "r") as json_file:
        data = json.load(json_file)

        # prende gli elementi innestati dentro a settings
        for obj in data['settings']:
            settings_value.append(obj)
        # while diff length between two vector add "None" to get vector
        while len(settings_value) < len(settings_list):
            settings_value.append("None")
        return settings_value


def create_settings_dict():
    try:
        settings_value = get_all_settings_values()
    except IOError:
        settings_value = ['None'] * n_settings
    return dict(zip(settings_list, zip(settings_value)))


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def getsettingspath():
    return os.path.dirname(os.path.realpath(__file__))
