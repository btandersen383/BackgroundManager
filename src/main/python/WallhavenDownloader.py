import wallhavenapi
import json
import random, string
import os
import time

from wallhavenapi import WallhavenApiV1

class WallhavenDownloader:
    def __init__(self, parent, ui, apiKey):
        self.apiKey = apiKey
        self.wallhavenApi = wallhavenapi.WallhavenApiV1(api_key=apiKey)
        self.result = None
        self.page = 1
        self.seed = 42
        self.data = []

        self.ui = ui
        self.parent = parent

        ui.wallhavenSaveButton.clicked.connect(self.onSave)
        ui.wallhavenApiKeyText.setText(apiKey)
        self.downloadDir = parent.settings.get("wallhaven_downloads")
        ui.wallhavenDownloadDirectoryText.setText(self.downloadDir)
        self.setSort(parent.settings.get("wallhaven_sort"))
        ui.wallhavenSortTypeText.setText(parent.settings.get("wallhaven_sort"))
        fil = parent.settings.get("wallhaven_filter")
        ui.wallhavenFilterText.setText(fil)
        fil = fil.split(" ")
        self.purity = []
        self.category = []
        self.setPurity(fil)
        self.setCategory(fil)


    def onSave(self):
        self.setApiKey(self.ui.wallhavenApiKeyText.text())
        self.setDownloadDir(self.ui.wallhavenDownloadDirectoryText.text())
        self.setSort(self.ui.wallhavenSortTypeText.text())
        fil = self.ui.wallhavenFilterText.text()
        filList = fil.split(" ")
        self.setPurity(filList)
        self.setCategory(filList)

        self.parent.settings.set("wallhaven_api_key", self.apiKey)
        self.parent.settings.set("wallhaven_downloads", self.downloadDir)
        self.parent.settings.set("wallhaven_sort", self.ui.wallhavenSortTypeText.text())
        self.parent.settings.set("wallhaven_filter", fil)
        self.parent.settings.save()
        print("wallhaven settings saved")


    def setPurity(self, purity):
        self.purity.clear()
        if "sfw" in purity:
            self.purity.append(wallhavenapi.Purity.sfw)
        if "sketchy" in purity:
            self.purity.append(wallhavenapi.Purity.sketchy)
        if "nsfw" in purity:
            self.purity.append(wallhavenapi.Purity.nsfw)


    def setCategory(self, category):
        self.category.clear()
        if "general" in category:
            self.category.append(wallhavenapi.Category.general)
        if "anime" in category:
            self.category.append(wallhavenapi.Category.anime)
        if "people" in category:
            self.category.append(wallhavenapi.Category.people)


    def setSort(self, sort):
        if sort == "random":
            self.sort = wallhavenapi.Sorting.random
        elif sort == "date_added":
            self.sort = wallhavenapi.Sorting.date_added
        elif sort == "top_list":
            self.sort = wallhavenapi.Sorting.toplist


    def setApiKey(self, apiKey):
        self.apiKey = apiKey
        self.wallhavenApi = wallhavenapi.WallhavenApiV1(api_key=apiKey)


    def setDownloadDir(self, downloadDir):
        self.downloadDir = downloadDir


    def setSeed(self, seed):
        if seed == "random":
            self.seed = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        else:
            self.seed = seed


    def search(self):
        self.result = self.wallhavenApi.search(categories=self.category,
                                           purities=self.purity,
                                           sorting=self.sort,
                                           page=self.page,seed=self.seed)
        self.data = self.result['data']
        self.page += 1


    def getDownload(self):
        if len(self.data) == 0:
            self.search()

        imageMeta = self.data.pop()
        imgId = imageMeta['id']
        fileType = imageMeta['file_type'].replace('image/','.')
        fileName = imgId + fileType
        filePath = os.path.join(self.downloadDir, fileName)
        self.wallhavenApi.download_wallpaper(imgId, filePath)
        finalPath = os.path.join(self.downloadDir,"wallhaven-{}".format(fileName))
        os.rename(filePath, finalPath)
        return finalPath
