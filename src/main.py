import sys
import logging
import ctypes

from PySide6.QtCore import (QCoreApplication)
from PySide6.QtWidgets import (QApplication)

from src.controllers.main_controller import MainController

try:
    # Include in try/except block if you're also targeting Mac/Linux
    myappid = 'mercuryseven.ssd.zextrasdrivedesktop.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

if __name__ == "__main__":

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

    controller = MainController(app)

    sys.exit(app.exec_())
