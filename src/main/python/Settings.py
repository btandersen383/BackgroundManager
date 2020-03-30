import json
from pathlib import Path
import os

from PyQt5.QtGui import QKeySequence, QPalette, QColor, QIcon, QTextBlock

class Settings:
    def __init__(self):
        """ Initialize the settings object """
        self.saveDir = "{}/snap/WallChanger".format(Path.home())
        self.saveFile = "{}/bgman.cfg".format(self.saveDir)
        # if the settings file does not exist, create it
        if not os.path.exists(self.saveFile):
            self.setDefaults()

        # read the settings file
        jsonFile = open(self.saveFile, "r")
        self.pySettings = json.loads(jsonFile.read())
        jsonFile.close()


    def __str__(self):
        jsonSettings = json.dumps(self.pySettings)
        return jsonSettings


    def setDefaults(self):
        """ Create the default settings file """
        if not os.path.exists(self.saveDir):
            os.mkdir(self.saveDir)

        if not os.path.exists(os.path.join(self.saveDir,"libs")):
            os.mkdir(os.path.join(self.saveDir,"libs"))

        if not os.path.exists(os.path.join(self.saveDir,"wallhaven")):
            os.mkdir(os.path.join(self.saveDir,"wallhaven"))

        pySettings = {
            "minimize_on_close":True,
            "dark_mode":True,
            "start_directory":os.path.expanduser("~/Pictures"),
            "rotate_on_start":True,
            "timer":20,
            "library_directory":os.path.join(self.saveDir,"libs"),
            "libraries":[],
            "default_library": "",
            "wallhaven_downloads":os.path.join(self.saveDir,"wallhaven"),
            "wallhaven_sort":"random",
            "wallhaven_filter":"general sfw sketchy", # purity and category
            "wallhaven_api_key":"",
            "system_picture_option":"scaled",
            "system_primary_color":"#000000"
        }

        jsonFile = open(self.saveFile, "w")
        jsonFile.write(json.dumps(pySettings))
        jsonFile.close()


    def save(self):
        jsonFile = open(self.saveFile, "w")
        jsonFile.write(json.dumps(self.pySettings))
        jsonFile.close()


    def get(self, name):
        return self.pySettings[name]


    def set(self, name, value):
        self.pySettings.update({name:value})

        # TODO: get dark mode working
        # if name == "dark_mode":
        #     if value:
        #         self.setDarkMode()
        #     else:
        #         # TODO: turn off dark mode
        #         pass


    def setDarkMode(self):
        """ Set dark mode for the user """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
