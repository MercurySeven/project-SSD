import sys
import logging
import view.icons

from PySide6.QtCore import (QCoreApplication, QSettings)
from PySide6.QtWidgets import (QApplication, QFileDialog)

from controllers import Controller
from view.system_tray_icon import SystemTrayIcon

if __name__ == "__main__":

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    # initialize settings
    env_settings = QSettings()

    # initialize logging format
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(filename)s:%(asctime)s:%(message)s")
    # rimuove i log spammosi di rete
    logging.getLogger("gql.transport.aiohttp").setLevel(logging.WARNING)
    logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)
    # settings.update_path(None) # debug

    # Controlliamo se l'utente ha già settato il PATH della cartella
    if not env_settings.value("sync_path"):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        # L'utente non ha selezionato la cartella
        if not dialog.exec_():
            env_settings.setValue("sync_path", None)
            sys.exit()

        sync_path = dialog.selectedFiles()
        if (len(sync_path) == 1):
            env_settings.setValue("sync_path", sync_path[0])
            env_settings.sync()
            print("Nuova directory: " + env_settings.value("sync_path"))

    controller = Controller()

    system_tray = SystemTrayIcon(":/icons/logo.png", app)
    system_tray.exit_option.triggered.connect(app.quit)
    system_tray.show_option.triggered.connect(controller.show_app)
    system_tray.show()

    sys.exit(app.exec_())
