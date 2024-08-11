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

        with open(screenshot.infoFile, "r") as infoFile:
            lastScreenshotTimeMS = int(infoFile.read())
        
        if not (lastScreenshotTimeMS and (not (stuff.getTimeMS() >= lastScreenshotTimeMS + screenshotFreqMS))):
            screenshotBin = screenshot.getScreenshotBinary()
            screenshotCreationTime = stuff.getTimeMS()
            screenshotDB.saveImage(screenshotBin, screenshotCreationTime)

            if stuff.info:
                print("Saved a screenshot")
                
            with open(screenshot.infoFile, "w") as infoFile:
                infoFile.write(str(lastScreenshotTimeMS + screenshotFreqMS))
        
        # Auto delete
        ...
