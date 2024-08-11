import os
import random
import stuff
import traceback
import waylandutil
from errors import DependencyMissingError
from PIL import ImageGrab

infoFile = f"{stuff.fileLocation}/.last.librerecall"

def makeFileIfNotExists() -> None:
    try:
        file = open(infoFile, "r")
    except:
        file = open(infoFile, "w")
        file.write(str(stuff.getTimeMS()))
    finally:
        if file:
            file.close()

def getPILScreenshotBin():
    screenshot = ImageGrab.grab()
    rawPath = f"{stuff.tmpPath}/{stuff.getTimeMS()}_image{random.randint(0, 100)}.png"
    path = stuff.getLocation(rawPath)
    screenshot.save(path)

    imgBin = None
    
    try:
        with open(path, "rb") as img:
            imgBin = img.read()
    finally:
        os.remove(path)

    return imgBin

def getWaylandScreenshotBin():
    if not stuff.waylandScreenshotUtil:
        raise DependencyMissingError("No supported screenshotting tool for Wayland available. Read \"Currently supported\" in the README.")

    return waylandutil.screenshotters[stuff.waylandScreenshotUtil]()

def getScreenshotBinary():
    screenshotBin = None
    if stuff.isWayland:
        try:
            screenshotBin = getWaylandScreenshotBin()
        except Exception as e:
            if not stuff.info:
                print("Falied to take a screenshot. This might be an issue with your compositor/screenshotting tool")
            else:
                print("Failed to take a screenshot")
                print(f"Screenshotting tool: {stuff.waylandScreenshotUtil}")
                print(f"Exception: {e}, {type(e)}")
                with open(".wayland_fail.log", "w") as f:
                    f.write(traceback.format_exc())
    else:
        screenshotBin = getPILScreenshotBin()

    if not screenshotBin:
        if stuff.info:
            print("Failed to take a screenshot")
        return None

    with open(infoFile, "w") as file:
        file.write(str(stuff.getTimeMS()))

    return screenshotBin
