import stuff
import random
import os
from PIL import ImageGrab

infoFile = "./.last.librerecall"

def makeFileIfNotExists() -> None:
    try:
        file = open(infoFile, "r")
    except:
        file = open(infoFile, "w")
        file.write(str(stuff.getTimeMS()))
    finally:
        if file:
            file.close()

def getScreenshotBinary():
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

    with open(infoFile, "w") as file:
        file.write(str(stuff.getTimeMS()))

    return imgBin
