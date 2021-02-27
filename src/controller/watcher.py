import time

from PySide6.QtCore import Signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import model.ssd_settings as ssd_settings


class Watcher:
    Sg_status = Signal(bool)
    is_running = False

    def __init__(self, path):

        # connect
        self.observer = Observer()
        self.path = path

    def run(self, watch):
        print("called watchdog")
        if not watch:
            if not self.is_running:
                print("Watchdog già disattivato")
            else:
                self.observer.unschedule_all()
                self.observer.stop()
                self.observer.join()
                print("disattiva watchdog thread")  # debug
                self.is_running = False
        else:
            if self.is_running:
                print("Watchdog già attivato")
            else:
                print("attiva thread watchdog")  # debug
                print("Controllo cartella: " + self.path)
                self.is_running = True
                self.background()

    def background(self):
        event_handler = Handler()
        # Lo richiamo ogni volta perchè non posso far ripartire lo stesso
        # thread
        self.observer = Observer()
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
        if event.event_type == "modified" or "created" or "deleted":
            print("Logging")
            # first i check if getpath returns a valid pathing
            path = ssd_settings.getpath()
            path_is_ok = ssd_settings.validate_path(path, "log.txt")
            if path_is_ok:
                path = ssd_settings.setup_path(path + "log.txt")
                with open(path, "w") as file:
                    file.write("True")
                    print("file modified with true")
                    print(path)
            else:
                print("Path not ok")
