import sys
from PySide6.QtWidgets import QApplication

from settings import Settings
from mainview import MainView
from model import Model
from controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create model and main view
    mainView = MainView()
    model = Model(Settings['REMOTE'], Settings['LOCAL'])

    # create controller
    controller = Controller(model, mainView)

    # show main view
    mainView.resize(800, 600)
    mainView.show()

    sys.exit(app.exec_())
