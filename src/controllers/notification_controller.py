from PySide6.QtWidgets import (QApplication)
from src.view.notification_view import NotificationView
from src.view.main_view import MainWindow


class NotificationController:

    def __init__(self, app: QApplication, view: MainWindow, username):
        self.notification_view = NotificationView(app)

        self.notification_view.exit_option.triggered.connect(app.quit)
        self.notification_view.show_option.triggered.connect(view.show)

        self.notification_view.show()

        # self.send_message("Bentornato %s" % username)

    def send_message(self, msg: str, duration: int = 4000) -> None:
        self.notification_view.show_message("SSD: Zextras Drive Desktop", msg, duration)
