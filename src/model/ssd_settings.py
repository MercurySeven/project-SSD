import os

# class SsdSettings:
# my module

path = None
file_name = "settings.mer"


def getpath():
    global path
    return path


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
            os.remove(old_full_path)
            with open(new_full_path, "w") as f:
                if len(file) > 3:
                    data[0] = new_path
                    f.writelines(data)
                    path = new_path
                else:
                    f.write(new_path + "\n")
                    f.write("None \n")  # new lines for other settings
                    f.write("None \n")
    except FileNotFoundError:
        # this means that there is no old settings file
        print(" Sono nell'eccezione ")
        with open(new_full_path, "w") as f:
            print(new_full_path)
            print("Ho aperto il nuovo file e ci scrivo dentro")
            f.write(new_path + "\n")
            f.write("None \n")  # new lines for other settings
            f.write("None \n")

# TODO refresh method done better


def refresh_path(self):
    file = open(self.path + "/" "settings.mer", "r")
    data = file.readlines()
    self.path = data[0]
    file.close()


def validate_path(path_to_validate, extra_to_attach=""):
    # i use two arguments because if i have to do path + filename and path is
    # None raises an exception, now i can firstly check if path is None and
    # then add them
    if path_to_validate is not None:
        with open(path_to_validate + extra_to_attach, "r"):
            return True
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
