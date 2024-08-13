import config
import screenshotDB
import screenshot
import time
import stuff
import os

def doWork():
    config.loadConfig()
    screenshotDB.makeConnection()
    screenshotFreqMS = config.get("SCREENSHOT_FREQUENCY_MS")
    screenshotFreqSeconds = screenshotFreqMS / 1000
    delay = screenshotFreqSeconds / 100

    try:
        os.remove(screenshot.file)
    except:
        pass

    screenshot.makeFileIfNotExists()

    while True:
        time.sleep(delay)

        # Screenshotting
        lastScreenshotTimeMS = None
        timeMS = stuff.getTimeMS()

        with open(screenshot.infoFile, "r") as infoFile:
            lastScreenshotTimeMS = int(infoFile.read())
        
        if not (lastScreenshotTimeMS and (not (timeMS >= lastScreenshotTimeMS + screenshotFreqMS))) and config.get("ENABLED"):
            screenshotBin = screenshot.getScreenshotBinary()
            screenshotCreationTime = timeMS
            screenshotDB.saveImage(screenshotBin, screenshotCreationTime)

            if stuff.info:
                print("Saved a screenshot")
                
            with open(screenshot.infoFile, "w") as infoFile:
                infoFile.write(str(screenshotCreationTime))
        
        # Auto delete
        autoDelType = config.get("AUTO_DELETE_TYPE")
        autoDelInterval = config.get("DELETE_AFTER_PERIOD")
        if autoDelType == "Disabled":
            continue
        
        baseTime = 3_600_000 if autoDelType == "Hours" else 86_400_000
        timeToDel = baseTime * autoDelInterval
        oldestAllowedTime = timeMS - timeToDel
        images = screenshotDB.getImages()

        for image in images:
            if int(image["date"]) < oldestAllowedTime:
                screenshotDB.deleteImage(image["id"])
                if stuff.info:
                    print("Deleted an image")
            else:
                break
