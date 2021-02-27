from PySide6.QtCore import Signal
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import model.ssd_settings as ssd_settings


class Watcher:
    Sg_status = Signal(bool)
    is_running = False

    def __init__(self, path):

        # connect
        # could be deleted, for now it's just to avoid Exceptions when turning
        # off
        self.observer = Observer()
        self.path = path

    def run(self, watch):
        print("called watchdog")
        self.path = ssd_settings.getpath()
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
        event_handler = MyHandler()
        # Lo richiamo ogni volta perchè non posso far ripartire lo stesso
        # thread
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

    def reboot(self):
        self.run(self, False)
        self.run(self, True)


class MyHandler(PatternMatchingEventHandler):
    currentEvent = ""
    update = False

    def __init__(self):
        super(
            MyHandler,
            self).__init__(
            ignore_patterns=[
                "*/log.mer",
                "*/settings.mer"])

    def log_event(self):
        event = self.currentEvent
        print("Logging")
        # first i check if getpath returns a valid pathing
        path: str = ssd_settings.getpath()
        if path is not None:
            path = ssd_settings.setup_path(path) + "log.mer"
            with open(path, "a+") as file:
                file.write(event + '\n')
        else:
            print("Path not ok")

    def on_modified(self, event):
        super(MyHandler, self).on_modified(event)
        if not event.is_directory:
            what = 'Directory' if event.is_directory else 'File'  # for future use
            self.currentEvent = what + ", modified, " + event.src_path
            self.log_event()

    def on_created(self, event):
        super(MyHandler, self).on_created(event)
        if not event.is_directory:
            what = 'Directory' if event.is_directory else 'File'
            self.currentEvent = what + ", created, " + event.src_path
            self.log_event()

    def on_deleted(self, event):
        super(MyHandler, self).on_deleted(event)
        if not event.is_directory:
            what = 'Directory' if event.is_directory else 'File'
            self.currentEvent = what + ", deleted, " + event.src_path
            self.log_event()

    def on_moved(self, event):
        super(MyHandler, self).on_moved(event)
        if not event.is_directory:
            what = 'Directory' if event.is_directory else 'File'
            self.currentEvent = what + ", moved, from: " + \
                event.src_path + ", to: " + event.dest_path
            self.log_event()

    def get_boolean(self, bool):
        self.update = bool
