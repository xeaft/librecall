import time
import os
from ConfigManager import ConfigManager
from DatabaseHandler import DatabaseHandler
from SystemInfo import SystemInfo
from Screenshotter import Screenshotter

def doWork():
    configManager = ConfigManager()
    sysInfo = SystemInfo()
    dbHandler = DatabaseHandler()

    dbHandler.makeConnection()
    screenshotFreqMS = configManager.get("SCREENSHOT_FREQUENCY_MS")
    screenshotFreqSeconds = screenshotFreqMS / 1000
    delay = screenshotFreqSeconds / 100

    sysInfo.makeInfoFileIfNotExists()

    screenshotter = Screenshotter()

    while True:
        time.sleep(delay)

        # Screenshotting
        lastScreenshotTimeMS = None
        timeMS = sysInfo.getTimeMS()

        with open(sysInfo.infoFile, "r") as infoFile:
            lastScreenshotTimeMS = int(infoFile.read())
        
        if not (lastScreenshotTimeMS and (not (timeMS >= lastScreenshotTimeMS + screenshotFreqMS))) and configManager.get("ENABLED"):
            screenshotBin = screenshotter.getScreenshot()
            screenshotCreationTime = timeMS
            dbHandler.saveImage(screenshotBin, screenshotCreationTime)

            if sysInfo.info:
                print("Saved a screenshot")
                
            with open(sysInfo.infoFile, "w") as infoFile:
                infoFile.write(str(screenshotCreationTime))
        
        # Auto delete
        autoDelType = configManager.get("AUTO_DELETE_TYPE")
        autoDelInterval = configManager.get("DELETE_AFTER_PERIOD")
        if autoDelType == "Disabled":
            continue
        
        baseTime = 3_600_000 if autoDelType == "Hours" else 86_400_000
        timeToDel = baseTime * autoDelInterval
        oldestAllowedTime = timeMS - timeToDel
        images = dbHandler.getImages()

        for image in images:
            if int(image["date"]) < oldestAllowedTime:
                dbHandler.deleteImage(image["id"])
                if sysInfo.info:
                    print("Deleted an image")
            else:
                break
    
    dbHandler.endConnection()
