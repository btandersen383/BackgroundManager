# Python library imports
from pathlib import Path
import os, sys, re, random

# QT5 library imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog)
from PyQt5 import uic
from PyQt5.QtGui import QIcon

# Local library imports
from WallChanger import Library, WallChanger
from Settings import Settings
from PreferencesWindow import PreferencesWindow
from SystemTray import SystemTrayIcon
from WallhavenDownloader import WallhavenDownloader

class Ui(QMainWindow):
    def __init__(self, uiFile, appctxt):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        self.ui = uic.loadUi(uiFile, self) # Load the .ui file
        self.appctxt = appctxt
        self.show() # Show the GUI

        # model objects
        self.settings = Settings()
        self.bgman = WallChanger()
        self.libraries = dict()
        self.paths = []

        # load the saved libraries
        libraryDirectory = self.settings.get("library_directory")
        for lib in self.settings.get("libraries"):
            library = Library()
            library.load(os.path.join(libraryDirectory, "{}.json".format(lib)))
            self.addLibrary(lib, library)

        # the opening directory when adding a path
        self.startDir = os.path.expanduser(self.settings.get("start_directory"))

        # set rotate on/off
        self.ui.startRotate.setChecked(self.settings.get("rotate_on_start"))

        # set up the timer to change backgrounds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onTriggerChange)
        self.timer.setInterval(self.settings.get("timer")*1000)
        if self.ui.startRotate.isChecked():
            self.timer.start()
        self.ui.rotateInterval.setValue(self.settings.get("timer"))

        # connect signals to slots
        # Menu actions
        self.ui.actionLoad_Library.triggered.connect(self.onLoadLibrary)
        self.ui.actionSave_Libraries.triggered.connect(self.onSaveLibraries)
        self.ui.actionPreferences.triggered.connect(self.onPreferences)

        # Top horizontal
        self.ui.libChoice.currentTextChanged.connect(self.onLibraryChange)
        self.ui.nextWallpaperButton.clicked.connect(self.onTriggerChange)
        self.ui.startRotate.toggled.connect(self.onStartRotate)
        self.ui.rotateInterval.valueChanged.connect(self.onIntervalChange)

        # Add Library Tab
        self.ui.addPathButton.clicked.connect(self.onAddPath)
        self.ui.addLibraryButton.clicked.connect(self.onAddLibrary)
        self.ui.removePathButton.clicked.connect(self.onRemovePath)

        # View Libraries Tab
        self.ui.deleteLibraryButton.clicked.connect(self.onDeleteLibrary)
        self.ui.editLibraryButton.clicked.connect(self.onEditLibrary)

        # Wallhaven Scrape Tab
        apiKey = self.settings.get("wallhaven_api_key")
        self.wallhavenScraper = WallhavenDownloader(self, self.ui, apiKey)

        # set the default librarie if it was loaded, do after full setup
        # TODO: add scrapers as libraries, need to check for call in onTriggerChange
        default = self.settings.get("default_library")
        if default in list(self.libraries.keys()):
            self.onLibraryChange(default)
        elif len(list(self.libraries.keys())) is not 0:
            key = random.choice(list(self.libraries.keys()))
            self.onLibraryChange(key)


    def onLoadLibrary(self):
        try:
            fileName = QFileDialog.getOpenFileName(
                self, "Open File", self.settings.get("library_directory"),
                "Json (*.json)")
            if fileName[0] is not '':
                library = Library()
                library.load(fileName[0])
                self.addLibrary(library.getName(), library)
        except Exception as e:
            print(e)


    def onSaveLibraries(self):
        for key in self.libraries:
            self.libraries[key].save(self.settings.get("library_directory"), key)
        keys = list(self.libraries.keys())
        self.settings.set("libraries", keys)
        self.settings.save()


    def onPreferences(self):
        testUi = self.appctxt.get_resource('preferencesWindow.ui')
        window = PreferencesWindow(self, testUi, self.settings)


    def onLibraryChange(self, library):
        # if user paused rotation, nothing should change wallpaper
        # but the library should still be allowed to change
        self.bgman.setLibrary(self.libraries[library])
        if not self.ui.startRotate.isChecked():
            return

        if library is not '':
            self.bgman.setWallpaper()
            self.timer.stop()
            self.timer.start()
        else:
            # the last library was deleted, clear set lib
            self.bgman.setLibrary(None)


    def fromWallhaven(self):
        file = self.wallhavenScraper.getDownload()
        self.bgman.setWallpaper(file)


    def fromLibrary(self):
        if self.bgman.getLibrary() is not None:
            try:
                self.bgman.setWallpaper()
            except Exception as e:
                print(e)


    # TODO: check if scraper library is set, use that scraper
    def onTriggerChange(self):
        self.timer.stop()
        if self.ui.startRotate.isChecked():
            self.timer.start()
        if self.ui.startScrapingWallhaven.isChecked():
            self.fromWallhaven()
        else:
            self.fromLibrary()


    def onStartRotate(self):
        if self.ui.startRotate.isChecked():
            self.timer.start()
        else:
            self.timer.stop()


    def onIntervalChange(self, time):
        self.timer.setInterval(time*1000)
        self.timer.stop()
        self.timer.start()


    def onAddPath(self):
        path = str(QFileDialog.getExistingDirectory(
            self, "Select Directory", self.startDir))
        if path is not '':
            self.paths.append(path)
            self.ui.addPathList.addItem(path)
            # reset the start directory for easier adds
            self.startDir = os.path.split(path)[0]


    def addLibrary(self, name, library):
        self.libraries.update({name: library})
        self.ui.libChoice.addItem(name)
        self.ui.addPathList.clear()
        self.ui.libraryNameText.clear()

        paths = "\t"+"\n\t".join(self.libraries[name].getDirectories())
        self.ui.viewLibraryList.addItem("Name: \t{}\nPaths: {}".format(name,paths))


    def isLegalName(self, name):
        if re.search("[^a-zA-Z0-9]", name) is not None:
            return False
        else:
            return True

    def onAddLibrary(self):
        name = self.ui.libraryNameText.text()
        if not self.isLegalName(name):
            print("name can only contain [a-zA-Z0-9]")
            return
        if name is '':
            print("Need to set a name")
            return
        if len(self.paths) == 0:
            print("Need to add a path")
            return
        lib = Library(name)
        for p in self.paths:
            lib.addPath(p)
        self.addLibrary(name, lib)
        self.paths.clear()


    def onRemovePath(self):
        selected = self.ui.addPathList.selectedItems()
        for sel in selected:
            row = self.ui.addPathList.row(sel)
            self.ui.addPathList.takeItem(row)


    def onDeleteLibrary(self):
        selected = self.ui.viewLibraryList.selectedItems()
        for sel in selected:
            # get the name of library to delete
            name = re.search("\t[a-zA-Z0-9]+\n", sel.text()).group(0).replace('\n', '').replace('\t', '')
            # delete it from the dict
            del(self.libraries[name])
            # remove it from the view list
            row = self.ui.viewLibraryList.row(sel)
            self.ui.viewLibraryList.takeItem(row)
            # remove it form the combo box
            idx = self.ui.libChoice.findText(name)
            self.ui.libChoice.removeItem(idx)


    def onEditLibrary(self):
        print("not done yet")


    def closeEvent(self, event):
        if self.settings.get("minimize_on_close"):
            self.hide()
            event.ignore()
        else:
            self.timer.stop()
            event.accept() # let the window close
