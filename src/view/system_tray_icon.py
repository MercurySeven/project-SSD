from PySide6.QtWidgets import (QSystemTrayIcon, QMenu)
from PySide6.QtGui import (QAction, QIcon)


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon_path: str, parent=None):
        """Custom SystemTrayIcon, richiede in input il path dell'icona"""
        QSystemTrayIcon.__init__(self, QIcon(icon_path), parent)
        self.setVisible(True)
        self.setToolTip("Zextras Drive Desktop")
        # self.showMessage("Mercury Seven", "Sembra che funzioni", msecs=5000)

        menu = QMenu()
        self.show_option = QAction("Mostra")
        self.exit_option = QAction("Esci")
        # TODO: Aggiungere l'opzione per acc/speg la sync dal menu

        menu.addAction(self.show_option)
        menu.addAction(self.exit_option)

        self.setContextMenu(menu)
