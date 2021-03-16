from PySide6.QtCore import (QObject, Signal)
from PySide6.QtWidgets import (QApplication)
from src.view.notification_view import NotificationView


class NotificationController(QObject):

    Sg_show_app = Signal()

    def __init__(self, app: QApplication, parent: QObject = None):
        super(NotificationController, self).__init__(parent)

        self.notification_view = NotificationView(app)

        self.notification_view.exit_option.triggered.connect(app.quit)
        self.notification_view.show_option.triggered.connect(
            lambda: self.Sg_show_app.emit())

        self.notification_view.show()

    def send_message(self, msg: str, duration: int = 1000):
        self.notification_view.show_message(
            "SSD: Zextras Drive Desktop", msg, duration)