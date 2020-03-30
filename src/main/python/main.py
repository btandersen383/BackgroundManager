#!/usr/bin/env python

# Python library imports
import os, sys

# QT5 library imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from SystemTray import SystemTrayIcon
from MainWindow import Ui

if __name__ == '__main__':

    app = QApplication(sys.argv)
    appctxt = ApplicationContext()

    testUi = appctxt.get_resource('mainWindow.ui')
    window = Ui(testUi, appctxt)

    planetsIcon = appctxt.get_resource('planets.png')
    trayIcon = SystemTrayIcon(QIcon(planetsIcon), window)
    trayIcon.show()

    sys.exit(app.exec_())
