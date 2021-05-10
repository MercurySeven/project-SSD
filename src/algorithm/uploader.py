
from threading import Thread

from PySide6.QtCore import Signal, QObject
from src.network.api import Api


class Uploader(QObject, Thread):
    signal_uploaded = Signal(QObject)

    def __init__(self, thread_name: str, file_path: str, _network: Api):
        Thread.__init__(self)
        QObject.__init__(self)

        self.setName(thread_name)
        self.setDaemon(True)

        self.file = file_path

        self.network = _network

    def run(self):
        # Override the run() function of Thread class
        print("Running %s" % self.name)
        # TODO: Realizzare upload
        self.signal_uploaded.emit(self)
