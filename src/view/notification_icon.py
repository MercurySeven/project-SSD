from PySide6.QtWidgets import (QSystemTrayIcon, QMenu)
from PySide6.QtGui import (QAction, QIcon)


class NotificationIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        """Custom SystemTrayIcon, richiede in input il path dell'icona"""
        QSystemTrayIcon.__init__(self, QIcon("./icons/logo.png"), parent)
        self.setVisible(True)
        self.setToolTip("Zextras Drive Desktop")

        menu = QMenu()
        self.show_option = QAction("Mostra")
        self.exit_option = QAction("Esci")
        # TODO: Aggiungere l'opzione per acc/speg la sync dal menu

        menu.addAction(self.show_option)
        menu.addAction(self.exit_option)

        self.setContextMenu(menu)

    def show_message(self, title: str, msg: str, duration: int = 1000):
        self.showMessage(title, msg, msecs=duration)
