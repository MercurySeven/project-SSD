import sys

from PySide6.QtCore import (QCoreApplication, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)

from controller.controller import Controller
from view.system_tray_icon import SystemTrayIcon

if __name__ == "__main__":

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

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
    controller = Controller()

    system_tray = SystemTrayIcon("logo.png", app)
    system_tray.exit_option.triggered.connect(app.quit)
    system_tray.show_option.triggered.connect(controller.show_app)
    system_tray.show()

    sys.exit(app.exec_())
