import os
import sys
import logging
import ctypes

from PySide2.QtCore import (QCoreApplication, QSettings)
from PySide2.QtWidgets import (QApplication, QFileDialog)

from src.controllers.login_controller import LoginController
from src.controllers.main_controller import MainController
from src.model.main_model import MainModel

if __name__ == "__main__":

    # Registro il processo per Windows, così da avere l'icona nella taskbar
    if sys.platform == "win32":
        try:
            myappid = 'mercuryseven.ssd.zextrasdrivedesktop.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(e)

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)
    # utile per avere l'icona di notifica
    app.setQuitOnLastWindowClosed(False)

    # initialize logging format
    _format = "%(asctime)s:%(levelname)s:%(filename)s:%(name)s:%(message)s"
    logging.basicConfig(level=logging.INFO, format=_format)
    # rimuove i log spammosi di rete
    logging.getLogger("gql.transport.aiohttp").setLevel(logging.WARNING)
    logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)

    env_settings = QSettings()

    # Controlliamo se l'utente ha già settato il PATH della cartella
    check_path = env_settings.value("sync_path")
    if not check_path or not os.path.isdir(check_path):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)  # provare anche .List
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.setOption(QFileDialog.DontResolveSymlinks)

        # L'utente non ha selezionato la cartella
        if not dialog.exec_():
            env_settings.setValue("sync_path", None)
            app.quit()

        sync_path = dialog.selectedFiles()
        if len(sync_path) == 1:
            env_settings.setValue("sync_path", sync_path[0])
            env_settings.sync()
            print("Nuova directory: " + env_settings.value("sync_path"))

    model = MainModel()
    controller = MainController(app, model)
    login_controller = LoginController(model, controller)
    sys.exit(app.exec_())
