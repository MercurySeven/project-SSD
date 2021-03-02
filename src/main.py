import sys
import logging
import view.icons

from PySide6.QtCore import (QCoreApplication)
from PySide6.QtWidgets import (QApplication, QFileDialog)

from controller.controller import Controller
from view.system_tray_icon import SystemTrayIcon
import settings

if __name__ == "__main__":

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    # initialize settings
    settings.check_file()

    # initialize logging format
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(filename)s:%(asctime)s:%(message)s")
    # Remove asyncio debug and info messages, but leave warnings.
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    # settings.update_path(None) # debug

    # Controlliamo se l'utente ha già settato il PATH della cartella
    if not settings.get_path():
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        # L'utente non ha selezionato la cartella
        if not dialog.exec_():
            settings.update_path(None)
            sys.exit()

        sync_path = dialog.selectedFiles()
        if (len(sync_path) == 1):
            settings.update_path(sync_path[0])
            print("Nuova directory: " + settings.get_path())

    controller = Controller()

    system_tray = SystemTrayIcon(":/icons/logo.png", app)
    system_tray.exit_option.triggered.connect(app.quit)
    system_tray.show_option.triggered.connect(controller.show_app)
    system_tray.show()

    sys.exit(app.exec_())
