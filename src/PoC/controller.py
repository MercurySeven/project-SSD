from PySide6.QtCore import QObject, Signal, Slot, Qt

from distutils.dir_util import copy_tree

import threading
import time
from settings import *
from mainview import *
from model import *

class Controller(QObject):

    Sg_status = Signal(bool)

    def __init__(self, model: Model, view: MainView, parent=None):
        super(Controller, self).__init__(parent)
    
        self.model = model
        self.view = view

        # connetto 
        self.view.syncWidget.Sg_sync.connect(self.__sync_daemon)

        self.Sg_status.connect(self.view.syncWidget.Sl_status)

        self.sync_job = None

        # return True if dirs content are not equal
        self.is_diff = lambda generator1, generator2: list(generator1) != list(generator2)
    
    @Slot(bool)
    def __sync_daemon(self, sync):
        
        if sync:
            self.sync_job = threading.Thread(target=self.sync, args=(Settings['TICK'],))
            self.sync_job.do_run = True
            self.sync_job.start()
            print("attiva thread di sincronizzazione") # debug
            self.Sg_status.emit(True)
        else:
            if self.sync_job:
                self.sync_job.do_run = False
                self.sync_job.join()
                print("disattiva thread di sincronizzazione") # debug
                self.Sg_status.emit(False)
    
    def sync(self, tick: int):
        """thread that synchronize directories"""
        t = threading.currentThread()
        while getattr(t, "do_run", True):

            print("sync job cycle...") # debug
            print(f"local content {list(self.model.local_content())}") # debug
            print(f"remote content {list(self.model.remote_content())}") # debug

            if self.is_diff(self.model.local_content(), self.model.remote_content()):

                if self.model.local_last_change() > self.model.remote_last_change():

                    # local -> remote
                    print("local -> remote") #debug
                    self.model.remote_clear()
                    copy_tree(self.model.local, self.model.remote)
                
                else:

                    # remote -> local
                    print("remote -> local") #debug
                    self.model.local_clear()
                    copy_tree(self.model.remote, self.model.local)
            #else sync

            print("end cicle\n") #debug
            time.sleep(tick)
        
        