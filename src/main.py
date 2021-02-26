import sys

from PySide6.QtCore import (QCoreApplication, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)

import model.ssd_settings as ssd_settings
from controller.controller import Controller

if __name__ == "__main__":

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)

    # initialize settings
    settings = QSettings()

    # settings.setValue("sync_path", None)  # debug

    # Controlliamo se l'utente ha già settato il PATH della cartella
    if not settings.value("sync_path"):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        # L'utente non ha selezionato la cartella
        if not dialog.exec_():
            settings.setValue("sync_path", None)
            sys.exit()

        sync_path = dialog.selectedFiles()
        if (len(sync_path) == 1):
            settings.setValue("sync_path", sync_path[0])
            print("Nuova directory: " + settings.value("sync_path"))
            # settings.sync() # save
    # impostazione della variabile setting, sarebbe da fare ad ogni modifica
    # del path
    ssd_settings.setpath(settings.value("sync_path"))
    controller = Controller()

    sys.exit(app.exec_())
