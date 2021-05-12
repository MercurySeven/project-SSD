from PySide6.QtWidgets import (QSystemTrayIcon, QMenu)
from PySide6.QtGui import (QAction, QIcon)

from src.view.stylesheets.qssManager import resource_path


class NotificationView(QSystemTrayIcon):

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, QIcon(resource_path("./assets/icons/logo.png")), parent)
        self.setVisible(True)
        self.setToolTip("SSD: Zextras Drive Desktop")

        menu = QMenu()
        self.show_option = QAction("Mostra")
        self.exit_option = QAction("Esci")

        menu.addAction(self.show_option)
        menu.addAction(self.exit_option)

        self.setContextMenu(menu)

    def show_message(self,
                     title: str,
                     msg: str,
                     duration: int = 1000,
                     icon: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.Information) -> None:
        self.showMessage(title, msg, msecs=duration, icon=icon)
