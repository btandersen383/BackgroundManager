# QT5 library imports
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu)

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        menu = QMenu(parent)
        nextAction = menu.addAction("&Next")
        nextAction.triggered.connect(parent.onTriggerChange)
        showAction = menu.addAction("&Show")
        showAction.triggered.connect(parent.show)
        exitAction = menu.addAction("&Exit")
        exitAction.triggered.connect(QApplication.quit)
        self.setContextMenu(menu)
