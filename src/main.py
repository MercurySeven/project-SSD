import sys
import logging

from PySide6.QtCore import (QCoreApplication)
from PySide6.QtWidgets import (QApplication)

from src.controllers.main_controller import MainController

if __name__ == "__main__":

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)
    # utile per avere l'icona di notifica
    app.setQuitOnLastWindowClosed(False)

    # initialize logging format
    _format = "%(levelname)s:%(filename)s:%(asctime)s:%(message)s"
    logging.basicConfig(level=logging.INFO, format=_format)
    # rimuove i log spammosi di rete
    logging.getLogger("gql.transport.aiohttp").setLevel(logging.WARNING)
    logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)

    controller = MainController(app)

    sys.exit(app.exec_())
