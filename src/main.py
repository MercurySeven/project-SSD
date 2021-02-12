import sys
from PySide6.QtWidgets import QApplication

from controller.controller import Controller
from model.server import API_Server
from settings import Settings

if __name__ == "__main__":

    # start fake remote server
    server = API_Server(Settings['HOST'], Settings['PORT'])
    server.run()

    # start main application
    app = QApplication(sys.argv)

    controller = Controller()

    sys.exit(app.exec_())
