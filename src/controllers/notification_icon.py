from PySide6.QtCore import (QObject, Signal, Slot)
from PySide6.QtWidgets import (QApplication)
from src.view.notification_icon import NotificationIcon


class NotificationIconController(QObject):

    Sg_app_quit = Signal()
    Sg_show_app = Signal()

    def __init__(self, app: QApplication, parent: QObject = None):
        super(NotificationIconController, self).__init__(parent)

        self.notification_view = NotificationIcon(app)

        self.notification_view.exit_option.triggered.connect(app.quit)
        self.notification_view.show_option.triggered.connect(
            lambda: self.Sg_show_app.emit())

        self.notification_view.show()

    def send_message(self, title: str, msg: str, duration: int = 1000):
        self.notification_view.show_message(title, msg, duration)
