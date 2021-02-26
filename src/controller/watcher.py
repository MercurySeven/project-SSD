import threading
import time

from PySide6.QtCore import Slot, QObject, Signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from settings import Settings


class Watcher(QObject):
    Sg_status = Signal(bool)

    def __init__(self, path, parent=None):

        super(Watcher, self).__init__(parent)
        # connect
        self.observer = Observer()
        self.path = path
        self.sync_job = None

    @Slot(bool)
    def __watchdog_daemon(self, watch):
        print("called watchdog")
        if watch:
            print("attiva thread watchdog")  # debug
        else:
            print("disattiva watchdog thread")  # debug

    def run(self, watch):
        print("called watchdog")
        if watch:
            print("attiva thread watchdog")  # debug
            self.sync_job = threading.Thread(
                target=self.background(), args=(Settings['TICK'],))
            self.sync_job.setDaemon(True)
            self.sync_job.do_run = True
            self.sync_job.start()
        else:
            self.sync_job.do_run = False
            self.sync_job.join()
            self.observer.stop()
            print("disattiva watchdog thread")  # debug
        # self.observer.join()

    def background(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        # if event.is_directory:
        #     return None
        print(
            "[{}] noticed: [{}] on: [{}] ".format(
                time.asctime(), event.event_type, event.src_path
            )
        )
