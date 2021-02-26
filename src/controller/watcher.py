import threading
import time

from PySide6.QtCore import QObject, Signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from settings import Settings


class Watcher(QObject):
    Sg_status = Signal(bool)

    observer_started = False
    is_running = False

    def __init__(self, path, parent=None):

        super(Watcher, self).__init__(parent)
        # connect
        self.observer = Observer()
        self.path = path
        self.sync_job = None

    def run(self, watch):
        print("called watchdog")
        if not watch:
            if not self.is_running:
                print("Watchdog già disattivato")
            else:
                self.sync_job.do_run = False
                self.sync_job.join()
                self.observer.unschedule_all()
                self.observer.stop()
                print("disattiva watchdog thread")  # debug
                self.is_running = False
        else:
            if self.is_running:
                print("Watchdog già attivato")
            else:
                print("attiva thread watchdog")  # debug
                self.sync_job = threading.Thread(
                    target=self.background(), args=(Settings['TICK'],))
                self.sync_job.setDaemon(True)
                self.sync_job.do_run = True
                self.sync_job.start()
                self.is_running = True

    def background(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        if not self.observer_started:
            self.observer.start()
            self.observer_started = True


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
