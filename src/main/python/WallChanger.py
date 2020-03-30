# Controls the changing of the background image and settings

import time, random, threading
import argparse
import os
import json

class WallChanger:
    """ Simple class to control changing the wallpaper """

    def __init__(self, pictureOption='scaled', primaryColor='#000000', library=None):
        """ Initialize variables and settings with defaults """
        self.pictureOption = pictureOption
        self.primaryColor = primaryColor
        self.library = library
        self.alsoSetScreensaver = False
        os.system("gsettings set org.gnome.desktop.background picture-options \"{}\""
            .format(self.pictureOption))
        os.system("gsettings set org.gnome.desktop.background primary-color \"{}\"".
            format(self.primaryColor))


    def setOptions(self, pictureOption=None, primaryColor=None, screensaver=None,
                    waitTime=None):
        """ Set and activate an option """
        if pictureOption is not None:
            self.pictureOption = pictureOption
            os.system("gsettings set org.gnome.desktop.background picture-options \"{}\""
                .format(self.pictureOption))

        if primaryColor is not None:
            self.primaryColor = primaryColor
            os.system("gsettings set org.gnome.desktop.background primary-color \"{}\""
                .format(self.primaryColor))

        if screensaver is not None:
            self.alsoSetScreensaver = screensaver


    def setLibrary(self, library):
        """ Set the active library """
        print("Setting library:\t{}".format(library))
        self.library = library


    def getLibrary(self):
        """ Return the active library object """
        return self.library


    def setWallpaper(self, path=None):
        """ Try to get a wallpaper from the library """
        try:
            if path is None:
                path = self.library.getNextWallpaper()
            print("Setting wallpaper:\t{}".format(path))
            os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri \""+path+"\"")
            if self.alsoSetScreensaver:
                os.system("/usr/bin/gsettings set org.gnome.desktop.screensaver picture-uri \""+path+"\"")
        except Exception as e:
            print("No next wallpaper! Exception: {}".format(e))



class Library:
    """ A container to hold and retrieve wallpaper file paths """

    allowableTypes = [".jpg", ".png", ".jpeg"]

    def __init__(self, name="default", dynamic=True, path=None):
        """ Initializer for a library object requires name and path """
        self.name = name
        self.dynamic = dynamic
        self.cycleAll = False
        self.fileList = []
        self.directoryList = []
        if path is not None:
            self.addPath(path)


    def __str__(self):
        return "Library {} with {} backgrounds".format(self.name, len(self.fileList))


    def getName(self):
        return self.name


    def setCycle(self, cycleAll):
        if cycleAll is True:
            self.toSee = [file for file in self.fileList]
            random.shuffle(self.toSee)
        self.cycleAll = cycleAll;


    def isAllowableFile(self, base, file):
        name, ext = os.path.splitext(file)
        if os.path.isfile(os.path.join(base, file)) and ext in Library.allowableTypes:
            return True
        else:
            return False


    def addPath(self, path):
        path = os.path.expanduser(path)
        if os.path.isfile(path):
            self.fileList.append(path)
        elif os.path.isdir(path):
            self.directoryList.append(path)
            base = path
            self.fileList += [os.path.join(base,file)
                            for file in os.listdir(base)
                            if self.isAllowableFile(base, file)]
        else:
            raise Exception("Path '{}' not acceptable.".format(path))


    def removePath(self, path):
        if path is None:
            self.fileList.clear()
        else:
            self.fileList.remove(path)


    def getFiles(self):
        return self.fileList


    def getDirectories(self):
        return self.directoryList


    def getNextWallpaper(self):
        if self.cycleAll is True:
            if len(self.toSee) is 0:
                self.toSee = self.fileList
                random.shuffle(self.toSee)
            return self.toSee.pop()
        else:
            return random.choice(self.fileList)


    def toJson(self):
        pyDict = {"name":self.name,
                 "dynamic":self.dynamic,
                 "cycleAll": self.cycleAll,
                 "directoryList": self.directoryList}
        if not self.dynamic:
            pyDict.update({"fileList": self.fileList})
        jsonDic = json.dumps(pyDict)
        return jsonDic


    def save(self, path=None, name=None):
        if path is None:
            path = os.getcwd()
        if name is None:
            name = self.name
        filePath = os.path.join(path, "{}.json".format(name))
        sfile = open(filePath, "w")
        sfile.write(self.toJson())
        sfile.close()


    def load(self, fileName):
        try:
            sfile = open(fileName, "r")
            pyDict = json.loads(sfile.read())
            self.name = pyDict["name"]
            self.dynamic = pyDict["dynamic"]
            self.cycleAll = pyDict["cycleAll"]
            if self.dynamic:
                for path in pyDict["directoryList"]:
                    self.addPath(path)
            else:
                self.fileList = pyDict["fileList"]
        except Exception as e:
            raise Exception("Unable to load library file: {}".format(fileName))


def main():
    library = Library("default", "~/Pictures")
    library.addPath("~/Pictures/test")
    print(library)
    print(library.toJson())
    library.save()
    exit()

    library.setCycle(True)
    changer = WallChanger(library=library)

    while True:
        changer.setWallpaper()
        time.sleep(60)


if __name__ == '__main__':
    main()
