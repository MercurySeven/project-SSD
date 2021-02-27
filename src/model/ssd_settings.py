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


def getquota():
    if path is None:
        raise FileNotFoundError
    else:
        full_path = setup_path(path) + file_name
        if validate_path(full_path):
            with open(full_path, "r") as file:
                if len(file.readlines()) > nSettings:
                    # makes pointer look at the beginning of file, readlines
                    # make pointer look at the eof
                    file.seek(0)
                    data = file.readlines()
                    if data[1] == "None":
                        return False
                    else:
                        return data[1]
                else:
                    return False
        else:
            raise FileNotFoundError


def setquota(quota):
    if path is None:
        raise FileNotFoundError
    else:
        full_path = setup_path(path) + file_name
        if validate_path(full_path):
            with open(full_path, "r") as file:
                if len(file.readlines) > nSettings:
                    file.seek(0)
                    data = file.readLines()
                    file.close()
                    with open(full_path, "w") as f:
                        data[1] = quota
                        f.writelines(data)
                else:
                    return False

        else:
            raise FileNotFoundError


def setpath(new_path):
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
            print(
                "Il path precedente non è ancora stato impostato, probabilmente prima avvio dell'app")
            raise FileNotFoundError
        old_full_path = setup_path(old_path) + file_name
        with open(old_full_path, "r") as file:
            data = file.readlines()
            file.seek(0)
            os.remove(old_full_path)
            with open(new_full_path, "w") as f:
                if len(file.readlines()) > nSettings:
                    file.seek(0)  # pointer look at beginning of file
                    data[0] = new_path
                    f.writelines(data)
                    path = new_path
                else:
                    f.write(new_path + "\n")
                    for i in range(nSettings):
                        f.write("None \n")  # new lines for other settings
    except FileNotFoundError:
        # this means that there is no old settings file
        print(" Sono nell'eccezione ")
        with open(new_full_path, "w") as f:
            print(new_full_path)
            print("Ho aperto il nuovo file e ci scrivo dentro")
            f.write(new_path + "\n")
            f.write("None \n")  # new lines for other settings
            f.write("None \n")
            path = new_path
    finally:
        print("----------")
        print(path)
        print("----------")

# TODO refresh method done better


def validate_path(path_to_validate, extra_to_attach=""):
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


def setup_path(path_to_fix):

    if not isinstance(path_to_fix, str):
        raise TypeError(
            "Passato un oggetto che non è una stringa come path al metodo setup_path")
    else:
        if not path_to_fix.endswith("/"):
            return path_to_fix + "/"
        else:
            return path_to_fix
