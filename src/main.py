import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication

from controller.controller import Controller

if __name__ == "__main__":

    # Bisogna fare questo per poter usare QSettings
    QCoreApplication.setOrganizationName("MercurySeven")
    QCoreApplication.setApplicationName("SSD")

    # start main application
    app = QApplication(sys.argv)

    controller = Controller()

    sys.exit(app.exec_())
