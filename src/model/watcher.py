from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import datetime

import model.ssd_settings as ssd_settings


class Watcher:
    """the Watcher class is used to activate or deactivate the watchdog thread, this is usually done automatically
    with signals or manually using the reboot method or run method
    """

    is_running = False

    def __init__(self, path):
        """
        Constructor for Watcher class, used to setup some public variables(path) and hidden
        :param path: the path that the watchdog will observe
        """

        # connect
        # could be deleted, for now it's just to avoid Exceptions when turning
        # off
        self.observer = Observer()
        self.path = path

    def run(self, watch):
        """
        method used to turn on or off the watchdog thread

        :param watch: boolean variable that is used to turn on the watchdog if true and off if false
        :return: True if the requested action was done and False if ignored (ex turning off when already off)
        """
        print("called watchdog")
        self.path = ssd_settings.getpath()
        if not watch:
            if not self.is_running:
                print("Watchdog già disattivato")
                return False
            else:
                self.observer.unschedule_all()
                self.observer.stop()
                self.observer.join()
                print("disattiva watchdog thread")  # debug
                self.is_running = False
                return True
        else:
            if self.is_running:
                print("Watchdog già attivato")
                return False
            else:
                print("attiva thread watchdog")  # debug
                print("Controllo cartella: " + self.path)
                self.is_running = True
                self.background()
                return True

    def background(self):
        """
        method used to initiate observer and start it

        :return: Nothing
        """
        event_handler = MyHandler()
        # Lo richiamo ogni volta perchè non posso far ripartire lo stesso
        # thread
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

    def reboot(self):
        """
        Method used to reboot the observer, turns it off and then on again

        :return: Nothing
        """
        self.run(False)
        self.run(True)


class MyHandler(PatternMatchingEventHandler):
    """
    Class used to handle all the events caught by the observer
    """

    currentEvent = ""
    update = False

    def __init__(self):
        """
        This constructor is used to setup which file needs to be ignored when caught by the observer
        """
        super(
            MyHandler,
            self).__init__(
            ignore_patterns=[
                "*/log.mer",
                "*/settings.mer"])

    def log_event(self):
        """
        Method that logs every event caught in a txt file, if the log file does not exists it creates one

        :return: Nothing
        """
        event = self.currentEvent
        print("Logging")
        print(ssd_settings.getquota())
        path: str = ssd_settings.getsettingspath()
        if path is not None:
            path = ssd_settings.setup_path(path) + "log.mer"
            # if this check returns false then there is no log file
            if ssd_settings.is_path_valid(path):
                # open file with append
                with open(path, "a+") as file:
                    file.write(event + '\n')
            else:
                # open file to override
                with open(path, "w+") as file:
                    file.write(event + '\n')
        else:
            # path is None, cannot do anything
            print("Path not ok")

    def on_modified(self, event):
        super(MyHandler, self).on_modified(event)
        what = 'Directory' if event.is_directory else 'File'  # for future use
        self.currentEvent = what + ", modified, " + \
            event.src_path + ", time, " + str(datetime.datetime.now())
        self.log_event()

    def on_created(self, event):
        super(MyHandler, self).on_created(event)
        what = 'Directory' if event.is_directory else 'File'  # for future use
        self.currentEvent = what + ", created, " + \
            event.src_path + ", time, " + str(datetime.datetime.now())
        self.log_event()

    def on_deleted(self, event):
        super(MyHandler, self).on_deleted(event)
        what = 'Directory' if event.is_directory else 'File'  # for future use
        self.currentEvent = what + ", deleted, " + \
            event.src_path + ", time, " + str(datetime.datetime.now())
        self.log_event()

    def on_moved(self, event):
        super(MyHandler, self).on_moved(event)
        what = 'Directory' if event.is_directory else 'File'
        self.currentEvent = what + ", moved, from: " + event.src_path + \
            ", to: " + event.dest_path + ", time, " + str(datetime.datetime.now())
        self.log_event()

    def get_boolean(self, bool):
        self.update = bool
