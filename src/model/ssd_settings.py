import os

# class SsdSettings:
# my module

path = None
file_name = "settings.mer"
nSettings = 2


def getpath():
    return path

# returns false if quota is not set, otherwise raise FileNotFoundError if
# it cannot find the settings.mer and if all goes well it returns the
# quota


def getquota() -> int:
    if path is None:
        raise FileNotFoundError("path is set to None, cannot search for settings file")
    else:
        full_path = setup_path(path) + file_name
        if is_path_valid(full_path):
            with open(full_path, "r") as file:
                if len(file.readlines()) >= nSettings:
                    # makes pointer look at the beginning of file, readlines
                    # make pointer look at the eof
                    file.seek(0)
                    data = file.readlines()
                    if data[1] == "None":
                        return False
                    else:
                        return int(data[1])
                else:
                    return False
        else:
            raise FileNotFoundError("Cannot find files in the following path" + full_path)


def setquota(quota: int) -> bool:
    int(quota)  # può lanciare ValueError
    if path is None:
        raise FileNotFoundError(
            "Root path is not set, cannot search for setting file")
    else:
        full_path = setup_path(path) + file_name
        if is_path_valid(full_path):
            with open(full_path, "r") as file:
                if len(file.readlines()) >= nSettings:
                    file.seek(0)
                    data = file.readlines()
                    file.close()
                    with open(full_path, "w") as f:
                        data[1] = quota
                        for obj in data:
                            f.write(str(obj))
                        return True
                else:
                    raise EOFError(
                        "File is not in the correct format, it does "
                        "not contain at least" + nSettings + "lines")

        else:
            raise FileNotFoundError(
                "Root path is set but setting file cannot be found or opened")

    return False


def setpath(new_path: str):
    global path  # God help me, used for the scope, long comment incoming to explain
    # in python module variable are global and can be read from wherever inside the module
    # but cannot be modified, doing global path and then assign
    # is a way to do it, even if risky
    old_path = path
    # with is used to properly close file at the end of code block even in
    # case of exceptions
    try:
        # preparo la stringa per il pathing nuovo e vecchio
        new_full_path = setup_path(new_path) + file_name
        if old_path is None:
            raise FileNotFoundError("Previous path not set, app just started")
        old_full_path = setup_path(old_path) + file_name
        with open(old_full_path, "r") as file:
            data = file.readlines()
            file.seek(0)
            os.remove(old_full_path)
            with open(new_full_path, "w") as f:
                if len(file.readlines()) >= nSettings:
                    file.seek(0)  # pointer look at beginning of file
                    data[0] = new_path
                    f.writelines(data)
                    path = new_path
                else:
                    f.write(new_path + "\n")
                    for i in range(nSettings):
                        f.write("None \n")  # new lines for other settings
    except FileNotFoundError as x:
        # this means that there is no old settings file
        print(x.strerror)
        if not is_path_valid(new_full_path):
            # Non esiste nemmeno un file nel nuovo path indicato quindi devo crearne uno nuovo
            # Questo dovrebbe capitare solo al primo avvio o quando uno
            # cancella le impostazioni
            write_new_settings_file([new_full_path, new_path, "None"])
        else:
            with open(new_full_path, "r") as f:
                if len(f.readlines()) >= nSettings:
                    # Il nuovo path ha il file up to date, non ha bisogno di
                    # essere sistemato
                    print("file is up to date")
                else:
                    # Il nuovo path ha il file con alcuni elementi mancanti,
                    # strano, file corrotto?
                    write_new_settings_file([new_full_path, new_path, "None"])
        path = new_path

    finally:
        print("----------")
        print(path)
        print("----------")

# maybe to a vector of strings to write


def write_new_settings_file(data: iter):
    # data in 1 = path, 2 = quota etc
    # data in 0 is the full path for the setting file
    try:
        iter(data)
        if isinstance(data, str):
            raise ValueError(
                "Wrong argument, passed a string when needed a list/vector of data")
        elif len(data < nSettings):
            raise ValueError(
                "Passed a vector with less than " + nSettings + "values")
    except TypeError:
        return ValueError(
            "Wrong argument, passed" + type(data) + "when needed a list/vector of data")
    else:
        with open(data[0], "w") as f:
            data.pop(0)  # rimuovo il path al file, non mi serve più
            print("Ho aperto il nuovo file e ci scrivo dentro")
            for setting in data:
                print(setting)
                f.write(setting + "\n")


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
