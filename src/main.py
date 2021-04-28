import sys
import logging
import ctypes

from PySide6.QtCore import (QCoreApplication)
from PySide6.QtWidgets import (QApplication)

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

    model = MainModel()
    controller = MainController(app, model)
    login_controller = LoginController(model, controller)
    sys.exit(app.exec_())
