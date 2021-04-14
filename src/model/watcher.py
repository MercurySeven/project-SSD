import logging
import os

from PySide6.QtCore import (QSettings, QObject, Signal)
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class Watcher(QObject):
    signal_event = Signal()
    """the Watcher class is used to activate or deactivate the watchdog thread,
    this is usually done automatically with signals or manually using
    the reboot method or run method
    """

    def __init__(self):
        super(Watcher, self).__init__()
        """
        Constructor for Watcher class, used to setup some public
        variables(path) and hidden
        :param path: the path that the watchdog will observe
        """

        # connect
        # could be deleted, for now it's just to avoid Exceptions when turning
        # off
        self.observer = Observer()
        env_settings = QSettings()

        self.path = lambda: env_settings.value("sync_path")

        # Debug < Info < Warning < Error so setting debug will get everything
        # I need to create a new logger cuz davide's logger is root log
        self.logger = logging.getLogger("watchdog")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(pathname)s:%(process)d:%(message)s')
        file_handler = logging.FileHandler('log.mer')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def run(self, watch):
        """
        method used to turn on or off the watchdog thread

        :param watch: boolean variable that is used to turn on
            the watchdog if true and off if false
        :return: True if the requested action was done and False
            if ignored (ex turning off when already off)
        """

        if watch:
            self.logger.info("Attivato watchdog")
            path = "" if self.path() is None else self.path()
            self.logger.info("Controllo cartella: " + path)
            return self.background()
        else:
            self.observer.unschedule_all()
            self.observer.stop()
            self.logger.info("Disattivato watchdog")
            return True

    def background(self):
        """method used to initiate observer and start it"""
        event_handler = MyHandler(self, self.logger)
        # Lo richiamo ogni volta perchè non posso far ripartire lo stesso
        # thread
        self.observer = Observer()
        self.observer.setName("Watchdog's thread")
        if self.path() is not None and os.path.isdir(self.path()):
            self.observer.schedule(event_handler, self.path(), recursive=True)
            self.observer.start()
            return True
        else:
            return False

    def reboot(self):
        """Method used to reboot the observer, turns it off and then on again"""
        self.run(False)
        self.run(True)


class MyHandler(PatternMatchingEventHandler, QObject):
    """
    Class used to handle all the events caught by the observer
    """

    def __init__(self, watchdog: Watcher, logger):
        """
        This constructor is used to setup which file needs to be ignored when
        caught by the observer
        """
        super(MyHandler, self).__init__(ignore_patterns=[
            "*/log.mer",
            "*/config.ini"])
        self.watchdog = watchdog
        self.logger = logger

    """def on_modified(self, event):
        super(MyHandler, self).on_modified(event)
        what = 'Directory' if event.is_directory else 'File'  # for future use
        self.logger.info(f"{what}, modified, {event.src_path}")"""

    def on_created(self, event):
        super(MyHandler, self).on_created(event)
        what = 'Directory' if event.is_directory else 'File'  # for future use
        self.logger.info(f"{what}, created, {event.src_path}")
        self.signal_watchdog()

    def on_deleted(self, event):
        super(MyHandler, self).on_deleted(event)
        what = 'Directory' if event.is_directory else 'File'  # for future use
        self.logger.info(f"{what}, deleted, {event.src_path}")
        self.signal_watchdog()

    def on_moved(self, event):
        super(MyHandler, self).on_moved(event)
        what = 'Directory' if event.is_directory else 'File'
        self.logger.info(
            f"{what}, moved, from: {event.src_path}, to: {event.dest_path}")
        self.signal_watchdog()

    def signal_watchdog(self):
        self.watchdog.signal_event.emit()
