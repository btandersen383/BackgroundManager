# Python library imports
from pathlib import Path
import os, sys, re, random

# QT5 library imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QDialog)
from PyQt5 import uic

# Local library imports
from Settings import Settings

class PreferencesWindow(QDialog):
    def __init__(self, parent, uiFile, settings):
        super(PreferencesWindow, self).__init__()
        self.ui = uic.loadUi(uiFile, self)
        self.show()

        self.settings = settings

        saveDirectory = settings.get("library_directory")
        defaultLibrary = settings.get("default_library")
        rotateInterval = settings.get("timer")
        minimizeOnClose = settings.get("minimize_on_close")
        darkMode = settings.get("dark_mode")
        rotateOnStart = settings.get("rotate_on_start")

        self.ui.librarySaveDirectoryText.setText(saveDirectory)
        self.ui.defaultLibraryText.setText(defaultLibrary)
        self.ui.rotateInterval.setValue(rotateInterval)
        self.ui.minimizeOnClose.setChecked(minimizeOnClose)
        self.ui.darkMode.setChecked(darkMode)
        self.ui.rotateOnStart.setChecked(rotateOnStart)


        self.ui.cancelButton.clicked.connect(self.onCancel)
        self.ui.saveButton.clicked.connect(self.onSave)

    def onSave(self):
        saveDirectory = self.ui.librarySaveDirectoryText.text()
        defaultLibrary = self.ui.defaultLibraryText.text()
        rotateInterval = self.ui.rotateInterval.value()
        minimizeOnClose = self.ui.minimizeOnClose.isChecked()
        darkMode = self.ui.darkMode.isChecked()
        rotateOnStart = self.ui.rotateOnStart.isChecked()

        self.settings.set("minimize_on_close", minimizeOnClose)
        self.settings.set("dark_mode", darkMode)
        self.settings.set("rotate_on_start", rotateOnStart)
        self.settings.set("timer", rotateInterval)
        self.settings.set("library_directory", saveDirectory)
        self.settings.set("default_library", defaultLibrary)
        self.settings.save()

        print("saved")
        self.close()

    def onCancel(self):
        print("canelling")
        self.close()
